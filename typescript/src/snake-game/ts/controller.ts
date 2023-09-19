import Model from './model';

class Controller {
  readonly #model: Model;
  constructor(model: Model) {
    this.#model = model;
  }

  turnLeft() {
    this.#model.turnAngle = -5;
  }

  turnRight() {
    this.#model.turnAngle = 5;
  }

  stopTurn() {
    this.#model.turnAngle = 0;
  }
}

export default Controller;
