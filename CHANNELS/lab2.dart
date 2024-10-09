abstract class Robot {
  String name;
  String status;
  int batteryLevel;

  Robot(this.name, this.status, this.batteryLevel);

  void moveTo(double x, double y);
}

class DeliveryRobot extends Robot {
  DeliveryRobot(String name) : super(name, 'вільний', 100);

  @override
  void moveTo(double x, double y) {
    print('$name is moving to ($x, $y)');
  }

  void recharge() {
    batteryLevel = 100;
    status = 'вільний';
  }

  bool isLowBattery() {
    return batteryLevel <= 10;
  }
}

abstract class RobotController {
  void start();
  void stop();
}

class DeliveryController implements RobotController {
  List<DeliveryRobot> robots = [];

  void addRobot(DeliveryRobot robot) {
    robots.add(robot);
  }

  @override
  void start() {
    for (var robot in robots) {
      robot.status = 'зайнятий';
    }
  }

  @override
  void stop() {
    for (var robot in robots) {
      robot.status = 'вільний';
    }
  }
}
