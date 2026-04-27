import zmq
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

CV_TIMEOUT_MS = 10_000

# CV side binds both sockets; bridge connects to them.
# This matches production: CV runs in Docker (stable binder),
# bridge runs natively on the robot (connects to CV's IP).
#
# CV side should use:
#   pull = ctx.socket(zmq.PULL)
#   pull.bind("tcp://*:5555")       # receives "stopped"
#   push = ctx.socket(zmq.PUSH)
#   push.bind("tcp://*:5556")       # bridge connects here to receive "ready"
#
# CV loop:
#   msg = pull.recv_string()        # blocks until bridge sends "stopped"
#   ... process image ...
#   push.send_string("ready")       # signal bridge to resume navigation
#
# Nav node calls the 'trigger_cv' service when it stops. The call blocks until
# CV responds (or times out); response.success indicates whether to resume.


class Bridge(Node):
    def __init__(self, push, pull):
        super().__init__('bridge')
        self._push = push
        self._pull = pull
        self.create_service(Trigger, 'trigger_cv', self._trigger_cv_cb)

    def _trigger_cv_cb(self, _request, response):
        self._push.send_string("stopped")

        if self._pull.poll(timeout=CV_TIMEOUT_MS):
            self._pull.recv_string()
            response.success = True
            response.message = ''
        else:
            self.get_logger().error("CV did not respond within timeout")
            response.success = False
            response.message = 'CV timeout'

        return response


def main():
    print("Starting bridge")
    rclpy.init()

    ctx = zmq.Context()
    # CV always runs in Docker on the same machine with -p 5555:5555 -p 5556:5556.
    # For testing, run the bridge container with --network=host so localhost
    # resolves to the host machine where cv_mock.py is running.
    push = ctx.socket(zmq.PUSH)
    push.connect("tcp://localhost:5555")

    pull = ctx.socket(zmq.PULL)
    pull.connect("tcp://localhost:5556")

    while pull.poll(timeout=0):
        pull.recv_string()

    node = Bridge(push, pull)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
