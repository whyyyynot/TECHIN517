#!/usr/bin/env python3
"""
Manipulation Node (string-based stub)

Publishes feedback lines such as
    "success true; status_code 0; message: Successfully picked apple"
so the orchestration node can parse them with simple substring checks.
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Empty
from custom_msgs.msg import PickCommand        # keep PickCommand interface


class ManipulationNode(Node):
    def __init__(self):
        super().__init__("manipulation_node")

        # Publishers (all String now)
        self.feedback_pub         = self.create_publisher(String, "/manipulation/feedback", 10)
        self.object_acquired_pub  = self.create_publisher(String, "/manipulation/object_acquired", 10)
        self.handoff_complete_pub = self.create_publisher(String, "/manipulation/handoff_complete", 10)

        # Subscribers
        self.create_subscription(PickCommand, "/manipulation/pick",  self.handle_pick_command, 10)
        self.create_subscription(Empty,        "/manipulation/handoff", self.handle_handoff_command, 10)

        # Internal state
        self.holding_object = False
        self.current_label  = None

        self.get_logger().info("Manipulation Node (string version) initialised")

    # ───────────────────────── Pick callback ──────────────────────────
    def handle_pick_command(self, msg: PickCommand):
        self.get_logger().info(f"Received pick for {msg.label}")

        # Simulated success
        self.holding_object = True
        self.current_label  = msg.label

        self._publish(
            self.feedback_pub,
            f"success true; status_code 0; message: Successfully picked {msg.label}"
        )
        self._publish(
            self.object_acquired_pub,
            f"success true; status_code 0; message: Object {msg.label} acquired"
        )

    # ──────────────────────── Handoff callback ────────────────────────
    def handle_handoff_command(self, _):
        if not self.holding_object:
            self._publish(
                self.feedback_pub,
                "success false; status_code 1; message: No object to hand off"
            )
            self.get_logger().error("Handoff failed – not holding any object")
            return

        label = self.current_label
        self.holding_object = False
        self.current_label  = None

        self._publish(
            self.feedback_pub,
            f"success true; status_code 0; message: Successfully handed off {label}"
        )
        self._publish(
            self.handoff_complete_pub,
            f"success true; status_code 0; message: Handoff of {label} complete"
        )

    # ───────────────────────── Helper function ────────────────────────
    def _publish(self, pub, text: str):
        msg = String()
        msg.data = text
        pub.publish(msg)
        self.get_logger().debug(f"Published → {pub.topic_name}: {text}")


def main(args=None):
    rclpy.init(args=args)
    node = ManipulationNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
