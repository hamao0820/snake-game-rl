import Food from './food';
import Judger from './judger';
import Score from './score';
import Snake from './snake';
import Stage from './stage';

class Model {
  readonly #snake: Snake;
  readonly #stage: Stage;
  readonly #score: Score;
  #food: Food | null = null;
  #gameOver = false;
  #turnAngle = 0;
  constructor() {
    this.#snake = new Snake();
    this.#stage = new Stage();
    this.#score = new Score();
    this.#food = this.createFood();
  }

  update(isCollisionSelf: boolean) {
    this.#snake.turn(this.#turnAngle);
    this.#snake.move();

    if (this.#food && Judger.checkCollisionFood(this.#snake, this.#food)) {
      this.#food = this.createFood();
      this.#snake.grow();
      this.#score.addScore();
      return;
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

  get food() {
    return this.#food;
  }

  get gameOver() {
    return this.#gameOver;
  }

  get score() {
    return this.#score.value;
  }
}

export default Model;
