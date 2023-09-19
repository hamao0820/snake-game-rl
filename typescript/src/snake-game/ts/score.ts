class Score {
  static #value: number = 0;

  static addScore() {
    this.#value += 10;
  }

  static get value() {
    return Score.#value;
  }
}

export default Score;
