import Food from './food';
import Judger from './judger';
import Score from './score';
import Snake from './snake';
import Stage from './stage';

class Model {
  readonly #snake: Snake;
  readonly #stage: Stage;
  readonly #score: Score;
  #foods: Food[] = [];
  #gameOver = false;
  #turnAngle = 0;
  constructor() {
    this.#snake = new Snake();
    this.#stage = new Stage();
    this.#score = new Score();
    this.#foods = Array.from({ length: 1 }, () => this.createFood());
  }

  update(isCollisionSelf: boolean) {
    this.#snake.turn(this.#turnAngle);
    this.#snake.move();

    const eatenFoodIndex = [];
    for (let i = 0; i < this.#foods.length; i++) {
      if (Judger.checkCollisionFood(this.#snake, this.#foods[i])) {
        eatenFoodIndex.push(i);
      }
    }

    for (const eatenIndex of eatenFoodIndex) {
      this.#foods[eatenIndex] = this.createFood();
      this.#score.addScore();
      this.snake.grow();
    }

    if (Judger.checkCollisionWall(this.#snake) || isCollisionSelf) {
      this.#gameOver = true;
    }
  }

  createFood() {
    const x = Math.random() * (Stage.Size - 2 * Snake.halfWidth) + Snake.halfWidth;
    const y = Math.random() * (Stage.Size - 2 * Snake.halfWidth) + Snake.halfWidth;
    return new Food(x, y);
  }

  set turnAngle(turnAngle: number) {
    this.#turnAngle = turnAngle;
  }

  get snake() {
    return this.#snake;
  }

  get stage() {
    return this.#stage;
  }

  get foods() {
    return this.#foods;
  }

  get gameOver() {
    return this.#gameOver;
  }

  get score() {
    return this.#score.value;
  }
}

export default Model;
