import Food from './food';
import Snake from './snake';
import Stage from './stage';

class Judger {
  static checkCollisionWall(snake: Snake) {
    return (
      snake.mx < Snake.halfWidth ||
      snake.mx >= Stage.Size - Snake.halfWidth ||
      snake.my < Snake.halfWidth ||
      snake.my >= Stage.Size - Snake.halfWidth
    );
  }

  static checkCollisionFood(snake: Snake, food: Food) {
    return (snake.mx - food.x) ** 2 + (snake.my - food.y) ** 2 <= ((Snake.halfWidth + 2) * 2) ** 2;
  }
}

export default Judger;
