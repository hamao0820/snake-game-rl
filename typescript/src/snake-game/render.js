const STAGE_SIZE = 240;
const SNAKE_HALF_WIDTH = 8;
class ScoreRenderer {
  #element;

  constructor() {
    this.#element = document.getElementById('score');
    this.#element.innerHTML = `Score: 0`;
  }

  render(score) {
    this.#element.innerText = `Score: ${score}`;
  }
}

class View {
  #ctx;
  constructor() {
    const canvas = document.getElementById('canvas');
    this.#ctx = canvas.getContext('2d');
  }
  renderStage() {
    this.#ctx.fillStyle = '#000';
    this.#ctx.fillRect(0, 0, STAGE_SIZE, STAGE_SIZE);
  }
  renderSnake(positionList, gameOver) {
    let i = 0;
    for (const [x, y] of positionList) {
      this.#ctx.fillStyle = gameOver ? '#800' : `hsl(${120 - (positionList.length - i) * 2}deg, 100%, 50%)`;
      this.#ctx.beginPath();
      this.#ctx.arc(x, y, SNAKE_HALF_WIDTH, 0, 2 * Math.PI);
      this.#ctx.fill();
      this.#ctx.closePath();
      i++;
    }
  }
  renderSnakeEye(mx, my, angle) {
    const lex = mx + Math.cos(((angle - 60) * Math.PI) / 180) * SNAKE_HALF_WIDTH * 0.4;
    const ley = my + Math.sin(((angle - 60) * Math.PI) / 180) * SNAKE_HALF_WIDTH * 0.4;
    const rex = mx + Math.cos(((angle + 60) * Math.PI) / 180) * SNAKE_HALF_WIDTH * 0.4;
    const rey = my + Math.sin(((angle + 60) * Math.PI) / 180) * SNAKE_HALF_WIDTH * 0.4;
    this.#ctx.fillStyle = '#fff';
    this.#ctx.beginPath();
    this.#ctx.arc(lex, ley, SNAKE_HALF_WIDTH * 0.4, 0, 2 * Math.PI);
    this.#ctx.fill();
    this.#ctx.closePath();
    this.#ctx.fillStyle = '#000';
    this.#ctx.beginPath();
    this.#ctx.arc(lex, ley, SNAKE_HALF_WIDTH * 0.2, 0, 2 * Math.PI);
    this.#ctx.fill();
    this.#ctx.closePath();
    this.#ctx.fillStyle = '#fff';
    this.#ctx.beginPath();
    this.#ctx.arc(rex, rey, SNAKE_HALF_WIDTH * 0.4, 0, 2 * Math.PI);
    this.#ctx.fill();
    this.#ctx.closePath();
    this.#ctx.fillStyle = '#000';
    this.#ctx.beginPath();
    this.#ctx.arc(rex, rey, SNAKE_HALF_WIDTH * 0.2, 0, 2 * Math.PI);
    this.#ctx.fill();
    this.#ctx.closePath();
  }
  renderFood(food) {
    if (food === null) {
      return;
    }
    this.#ctx.fillStyle = `hsl(${Math.random() * 360}, 100%, 50%)`;
    this.#ctx.beginPath();
    this.#ctx.arc(food.x, food.y, SNAKE_HALF_WIDTH, 0, 2 * Math.PI);
    this.#ctx.fill();
    this.#ctx.closePath();
  }
  render(positionList, gameOver, foods, mx, my, angle) {
    this.renderStage();
    this.renderSnake(positionList, gameOver);
    this.renderSnakeEye(mx, my, angle);
    for (const food of foods) this.renderFood(food);
  }
  get ctx() {
    return this.#ctx;
  }
}

const scoreRenderer = new ScoreRenderer();
const view = new View();
