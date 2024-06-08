#include <ros/ros.h>
#include <std_msgs/Bool.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Float32MultiArray.h>
#include <geometry_msgs/Vector3.h>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <ros/package.h>  // Include this header for ros::package::getPath

class FlowerCore {
public:
    FlowerCore() {
        // Subscriber
        servo_end_sub = nh.subscribe("servo_end", 10, &FlowerCore::servoEndCallback, this);
        robot_end_sub = nh.subscribe("robot_end", 10, &FlowerCore::robotEndCallback, this);
        diff_yaw_sub = nh.subscribe("diff_yaw", 10, &FlowerCore::diffYawCallback, this);
        
        // Publisher
        phi_pub = nh.advertise<std_msgs::Float32>("phi", 10);
        sound_command_pub = nh.advertise<std_msgs::Int16>("sound_command", 10);
        led_command_pub = nh.advertise<std_msgs::Float32MultiArray>("led_command", 10);
        robot_command_pub = nh.advertise<geometry_msgs::Vector3>("robot_command", 10);

        // CSV file processing
        readDesignCSV();
        processCSVData();
        performanceFirstSetup();
    }

    void readDesignCSV() {
        // Get the package path
        std::string package_path = ros::package::getPath("flower_core");
        // Construct the full path to the CSV file
        std::string file_path = package_path + "/flower_designer/design.csv";
        
        std::ifstream file(file_path);
        if (!file.is_open()) {
            ROS_ERROR("Failed to open file: %s", file_path.c_str());
            return;
        }

        std::string line, cell;
        while (std::getline(file, line)) {
            if (line.empty()) {
                continue; // Skip empty lines
            }

            std::vector<std::string> row;
            std::stringstream lineStream(line);

            while (std::getline(lineStream, cell, ',')) {
                row.push_back(cell);
            }

            design_data.push_back(row);
        }
        file.close();
    }

    void processCSVData() {
        int current_step_size = 0;

        for (const auto& row : design_data) {
            if (!row[0].empty() && !row[1].empty()) {
                // r and n row
                try {
                    float r = std::stof(row[0]);
                    float n = std::stof(row[1]);
                    sequence_meta.push_back({abs(r), n});
                    
                    // Store current step size and reset it
                    if (current_step_size > 0) {
                        step_sizes.push_back(current_step_size);
                        current_step_size = 0;
                    }
                } catch (const std::invalid_argument& e) {
                    ROS_ERROR("Invalid argument: %s", e.what());
                } catch (const std::out_of_range& e) {
                    ROS_ERROR("Out of range: %s", e.what());
                }
            } else if (row.size() > 2 && row[2] != "diff_yaw") { // Skip the header row
                // Other data row
                std::vector<float> data;
                try {
                    for (size_t i = 2; i < row.size(); ++i) {
                        if (!row[i].empty()) {
                            data.push_back(std::stof(row[i]));
                        }
                    }
                    performance_array.push_back(data);
                    current_step_size++;
                } catch (const std::invalid_argument& e) {
                    ROS_ERROR("Invalid argument: %s", e.what());
                } catch (const std::out_of_range& e) {
                    ROS_ERROR("Out of range: %s", e.what());
                }
            }
        }

        // Add the last step size if there were no more r, n rows
        if (current_step_size > 0) {
            step_sizes.push_back(current_step_size);
        }

        // Print the arrays to the console
        ROS_INFO("Sequence Meta Data:");
        float last_r = 0;
        for (const auto& meta : sequence_meta) {
            ROS_INFO("r: %f, n: %f", meta[0], meta[1]);
            if (meta[0] - last_r > 0.01) robot_command_array.push_back({0, meta[0] - last_r,0}); //直進
            robot_command_array.push_back({1, meta[1], meta[0]}); //旋回
            last_r = meta[0];
        }

        ROS_INFO("Performance Data:");
        for (const auto& data : performance_array) {
            std::ostringstream oss;
            for (const auto& val : data) {
                oss << val << ", ";
            }
            ROS_INFO("%s", oss.str().c_str());
        }

        // Print the step sizes
        ROS_INFO("Step Sizes:");
        for (const auto& size : step_sizes) {
            ROS_INFO("%d", size);
        }
    }


    void performanceFirstSetup() {
        //LED指令
        std_msgs::Float32MultiArray led_command;
        led_command.data.clear();
        led_command.data.push_back(performance_array[0][4]);
        led_command.data.push_back(performance_array[0][5]);
        led_command.data.push_back(performance_array[0][6]);
        led_command.data.push_back(performance_array[0][7]);
        led_command.data.push_back(performance_array[0][8]);
        led_command.data.push_back(performance_array[0][9]);
        led_command.data.push_back(performance_array[0][10]);
        led_command_pub.publish(led_command);

        //サーボ指令(負)
        std_msgs::Float32 phi;
        phi.data = -performance_array[0][3];
        phi_pub.publish(phi);

        //robot_endをtrueに
        robot_end = true;
    }

    void servoEndCallback(const std_msgs::Bool::ConstPtr& msg) {
        if(robot_end==false) servo_end = true;
        else {
            // robot_endが1ならシーケンスを1進めてrobot_endとserbo_endをfalseに
            sequence++;
            robot_end = false;
            // ロボットに指定を出す
            geometry_msgs::Vector3 robot_command;
            robot_command.x = robot_command_array[sequence-1][0];
            robot_command.y = robot_command_array[sequence-1][1];
            robot_command.z = robot_command_array[sequence-1][2];
            robot_command_pub.publish(robot_command);
            if(sequence%2>0.5){//旋回シーケンス
                //やることなし
            }
            else{//直進シーケンス
                // LED消す
                std_msgs::Float32MultiArray led_command;
                led_command.data.clear();
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command_pub.publish(led_command);
                // サーボに負の値で指令を出す
                std_msgs::Float32 phi;
                phi.data = -performance_array[sequence/2*step_sizes[sequence/2]][3];
                phi_pub.publish(phi);
            }
        }
    }

    void robotEndCallback(const std_msgs::Bool::ConstPtr& msg) {
        if(servo_end==false) robot_end = true;
        else{ 
            // servo_endが1ならシーケンスを1進めてrobot_endとserbo_endをfalseに
            sequence++;
            servo_end = false;
            // ロボットに指定を出す
            geometry_msgs::Vector3 robot_command;
            robot_command.x = robot_command_array[sequence-1][0];
            robot_command.y = robot_command_array[sequence-1][1];
            robot_command.z = robot_command_array[sequence-1][2];
            robot_command_pub.publish(robot_command);
            if(sequence%2>0.5){//旋回シーケンス
                //やることなし
            }
            else{//直進シーケンス
                // LED消す
                std_msgs::Float32MultiArray led_command;
                led_command.data.clear();
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command.data.push_back(0.0f);
                led_command_pub.publish(led_command);
                // サーボに負の値で指令を出す
                std_msgs::Float32 phi;
                phi.data = -performance_array[sequence/2*step_sizes[sequence/2]][3];
                phi_pub.publish(phi);
            }
        }
    }

    void diffYawCallback(const std_msgs::Float32::ConstPtr& msg) {
        if(sequence%2>0.5){// 旋回シーケンスなら実行
            // ステップidの更新
            float diff_yaw = msg->data;
            int current_step = 0;
            int look_ahead = 3;
            for(int step = 0; step < step_sizes[sequence/2]; step++){
                if(diff_yaw<performance_array[sequence/2*step_sizes[sequence/2]+step][2]){
                    current_step = step + look_ahead;
                    if(current_step >= step_sizes[sequence/2]) current_step = step_sizes[sequence/2]-1;
                    break;
                }
            }

            // ステップに応じたperformanceのpublish
            std_msgs::Float32 phi;
            phi.data = performance_array[sequence/2*step_sizes[sequence/2]+current_step][3];
            phi_pub.publish(phi);

            std_msgs::Float32MultiArray led_command;
            led_command.data.clear();
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][4]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][5]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][6]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][7]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][8]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][9]);
            led_command.data.push_back(performance_array[sequence/2*step_sizes[sequence/2]+current_step][10]);
            led_command_pub.publish(led_command);

            // std_msgs::Int16 sound_command;
            // sound_command.data = ...;
            // sound_command_pub.publish(sound_command);
        }
    }

private:
    ros::NodeHandle nh;
    ros::Subscriber servo_end_sub;
    ros::Subscriber robot_end_sub;
    ros::Subscriber diff_yaw_sub;

    ros::Publisher phi_pub;
    ros::Publisher sound_command_pub;
    ros::Publisher led_command_pub;
    ros::Publisher robot_command_pub;

    std::vector<std::vector<std::string>> design_data;
    std::vector<std::vector<float>> sequence_meta;
    std::vector<std::vector<float>> performance_array;
    std::vector<std::vector<float>> robot_command_array;
    std::vector<int> step_sizes;
    bool robot_end = false;
    bool servo_end = false;
    int sequence = 0;
    float led_setup[7];
};

int main(int argc, char **argv) {
    ros::init(argc, argv, "flower_core");
    FlowerCore flowerCore;
    ros::spin();
    return 0;
}
