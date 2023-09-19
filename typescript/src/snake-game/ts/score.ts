class Score {
  #value: number;

  constructor() {
    this.#value = 0;
  }

  addScore() {
    this.#value += 10;
  }

  get value() {
    return this.#value;
  }
}

export default Score;
