/**
 * @jest-environment jsdom
 */

const fs = require("fs");
const path = require("path");

describe("Jogo da Memória", () => {
  let document;

  beforeEach(() => {
    const html = fs.readFileSync(
      path.resolve(__dirname, "../templates/memory.html"),
      "utf8"
    );
    document = new DOMParser().parseFromString(html, "text/html");
    global.document = document;
    global.window = document.defaultView;
  });

  test("tabuleiro deve existir no DOM", () => {
    const board = document.querySelector("#memory-board");
    expect(board).not.toBeNull();
  });

  test("deve haver botão de reinício", () => {
    const btn = document.getElementById("restart-btn");
    expect(btn).not.toBeNull();
    expect(btn.textContent.toLowerCase()).toContain("reiniciar");
  });

  test("placar deve mostrar acertos e tentativas", () => {
    const score = document.getElementById("scoreboard");
    expect(score.textContent.toLowerCase()).toMatch(/acertos/i);
    expect(score.textContent.toLowerCase()).toMatch(/tentativas/i);
  });
});
