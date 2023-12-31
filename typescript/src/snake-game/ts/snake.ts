import Stage from './stage';

class Snake {
  static readonly initialLength = 150;
  static readonly halfWidth = 8;
  readonly #positionList: [number, number][] = [];
  #mx = Stage.Size / 2;
  #my = (Stage.Size * 4) / 5;
  #speed = 1;
  #angle = -90;
  #maxHP = 100;
  #hp = this.#maxHP;

  constructor() {
    for (let i = 0; i < Snake.initialLength; i++) {
      this.#positionList.push([this.#mx, this.#my]);
    }
  }

  turn(turnAngle: number) {
    this.#angle += turnAngle;
  }

  move() {
    this.#mx += this.#speed * Math.cos((this.#angle * Math.PI) / 180);
    this.#my += this.#speed * Math.sin((this.#angle * Math.PI) / 180);
    this.#positionList.push([this.#mx, this.#my]);
    this.#positionList.shift();
    if (this.#hp > 0) this.#hp--;
  }

  grow() {
    const tailPosition = this.#positionList[0];
    for (let i = 0; i < 30; i++) {
      this.#positionList.unshift(tailPosition);
    }
    this.#maxHP += 15;
    this.#hp = this.#maxHP;
  }

  get positionList() {
    return this.#positionList;
  }

  get angle() {
    return this.#angle;
  }

  get mx() {
    return this.#mx;
  }

  get my() {
    return this.#my;
  }

  get hp() {
    return this.#hp;
  }
}

export default Snake;
