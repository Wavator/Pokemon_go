#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <geometry_msgs/Twist.h>
#include <string>

using namespace std;
using namespace cv;

static const bool DEBUG = false;
static const bool MOVE = true;

class PokemonCatching
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  int flag = 1;
  int roi_tl_x;
  int roi_tl_y;
  int roi_br_x;
  int roi_br_y;
  int roi_height;
  int roi_width;
  int exit = 0;
  // string folder_path = "/home/wzl/pokemon_ws/";


public:
  PokemonCatching()
    : it_(nh_)
  {
    // Subscribe modified video stream from pokemon_searching
    image_sub_ = it_.subscribe("tb3_0/pokemon_go/searcher", 1, &PokemonCatching::imageCb, this);
  }

  ~PokemonCatching()
  {
    // cv::destroyWindow(OPENCV_WINDOW);
  }

  static bool cmp(Point a,Point b){
    if(a.x == b.x){
      return a.y<b.y;
    }
    return a.x<b.x;
  }


  void detectRect(cv_bridge::CvImagePtr & cv_ptr){
    Mat threshold_output;
    vector<vector<Point> > contours;
    vector<Point> contours_point;
    vector<vector<Point> > all_contours;
    vector<vector<Point> > pokemon_contours;
    vector<Point> all_contours_point;
    vector<Vec4i> hierarchy;
    Mat src_gray;
    Mat frame;
    //自定义形态学元素结构
    cv::Mat element5(9, 9, CV_8U, cv::Scalar(1));//5*5正方形，8位uchar型，全1结构元素  
    Scalar color = Scalar(0,255,0);
    Scalar outColor = Scalar(0,0,255);
    cv::Mat closed;
    Rect rect;
    Rect rect1;

    frame = cv_ptr->image;
    Rect roiRect(roi_tl_x, roi_tl_y, roi_width, roi_height);
    Mat roi = frame(roiRect);
    Mat image;
    Mat image2;
    Mat image3;
    if(DEBUG){
		  image = roi.clone();
		  image2 = roi.clone();
		  image3 = roi.clone();
    }

    cvtColor(roi, src_gray, COLOR_BGR2GRAY);  //颜色转换

    Canny(src_gray, threshold_output, 85, 140, (3, 3));   //使用Canny检测边缘
    cv::morphologyEx(threshold_output, closed, cv::MORPH_CLOSE, element5);  //形态学闭运算函数  

    if(DEBUG){
      imshow("canny", threshold_output);
      // waitKey();
      imshow("erode", closed);
      // waitKey(3);
    }
    findContours(closed, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE, Point());
    
    rect = boundingRect(contours[contours.size()-1]);
    

  
    // move
    if(MOVE){
      

      
        
        char *env_val = getenv("CMAKE_PREFIX_PATH");
        char *pathx = strstr(env_val, "/");
        char *pathy = strstr(env_val, "devel");
        int len = pathy - pathx + 1;
        char *fpath = (char*)malloc((len) * sizeof(char));
        memcpy(fpath, pathx, len - 1);
        fpath[len-1] = '\0';
        string folder_path(fpath);

        ROS_INFO("CATCH");
        exit = 1;

        // search and draw pokemon border
        findContours(closed, pokemon_contours, hierarchy,  RETR_TREE, CHAIN_APPROX_NONE, Point());
        rect1 = boundingRect(pokemon_contours[0]);
        int rect1_tl_x;
        int rect1_tl_y;
        int rect1_br_x;
        int rect1_br_y;
        int diff = 6;
        if((abs(rect1.tl().x-rect.tl().x)<=2)){
          rect1_tl_x = rect1.tl().x + diff;
        }else{
          rect1_tl_x = rect1.tl().x;
        }
        if((abs(rect1.tl().y-rect.tl().y)<=2)){
          rect1_tl_y = rect1.tl().y + diff;
        }else{
          rect1_tl_y = rect1.tl().y;
        }
        if((abs(rect1.br().x-rect.br().x)<=2)){
          rect1_br_x = rect1.br().x - diff;
        }else{
          rect1_br_x = rect1.br().x;
        }
        if((abs(rect1.br().y-rect.br().y)<=2)){
          rect1_br_y = rect1.br().y - diff;
        }else{
          rect1_br_y = rect1.br().y;
        }
        Rect newRect1(rect1_tl_x, rect1_tl_y, rect1_br_x-rect1_tl_x, rect1_br_y-rect1_tl_y);
        rectangle(roi,newRect1,color, 2);
        // draw picture border

        rectangle(roi,rect, outColor, 2);
        // rectangle(frame, cv::Point(roi_tl_x, roi_tl_y), cv::Point(roi_br_x, roi_br_y), CV_RGB(255,0,0));

        // save img
        vector<cv::String> file_names;
        vector<string> split_string;
        glob(folder_path, file_names);

        int pokemon_img_num = 0;
        for (int i = 0; i < file_names.size(); i++) {
          // ROS_INFO("filename: %s", file_names[i].c_str());
          int pos = file_names[i].find_last_of("/");
          string file_name(file_names[i].substr(pos + 1));
          if(file_name.compare(0, 7, "pokemon")==0){
            pokemon_img_num++;
          }
        }
        pokemon_img_num ++;
        string file_name = folder_path + "pokemon_" + to_string(pokemon_img_num) + ".jpg";
        imwrite(file_name, frame);
        ros::shutdown();

        return;
      
    }
    if(!MOVE)
      exit = 1;
    // image_sub_.shutdown();
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    // ROS_INFO("redy to detect ");
    if(flag==1){
      int height = cv_ptr->image.rows;
      int width = cv_ptr->image.cols;
      roi_tl_x = width/3;
      roi_tl_y = height/16;
      roi_br_x = 2*width/3;
      roi_br_y = 5*height/8;
      roi_height = roi_br_y-roi_tl_y;
      roi_width = roi_br_x-roi_tl_x;
      flag = 5;

    }
    if(exit!=1)
      detectRect(cv_ptr);
    
    // test 1*1 半格
    if(flag == 2){
      ROS_INFO("detect finish");
      // ros::Rate loopRate(10);
      geometry_msgs::Twist speed;
      // // x前后线速度 z左右旋转角速度
      speed.linear.x=1;
      // // speed.angular.z=0/30; 
      //vel_pub_.publish(speed); 
      ros::Duration(1).sleep(); 
      //vel_pub_.publish(geometry_msgs::Twist()); 
      flag = 0;
    }

  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "pokemon_catching");
  PokemonCatching pc;
  ros::spin();
  return 0;
}
