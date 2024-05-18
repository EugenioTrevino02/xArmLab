import rclpy
from rclpy.node import Node
import tf2_ros
import geometry_msgs.msg
import visualization_msgs.msg


class TFListener(Node):

    def __init__(self):
        super().__init__('tf_listener')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.marker_publisher = self.create_publisher(visualization_msgs.msg.Marker, '/visualization_marker', 10)
        self.marker_id = 0
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        try:
            transform = self.tf_buffer.lookup_transform('link_base', 'link_eef', rclpy.time.Time())
            marker = visualization_msgs.msg.Marker()
            marker.header.frame_id = 'world'
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.type = visualization_msgs.msg.Marker.SPHERE
            marker.action = visualization_msgs.msg.Marker.ADD
            marker.id = self.marker_id
            self.marker_id += 1
            marker.pose.position.x = transform.transform.translation.x
            marker.pose.position.y = transform.transform.translation.y
            marker.pose.position.z = transform.transform.translation.z
        
            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = 0.05
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0
            self.marker_publisher.publish(marker)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException) as e:
            self.get_logger().error(f"Failed to lookup transform: {e}")


def main(args=None):
    rclpy.init(args=args)
    tf_listener = TFListener()
    rclpy.spin(tf_listener)
    tf_listener.destroy_node()
    rclpy.shutdown()


if __name__== '__main__':
    main()