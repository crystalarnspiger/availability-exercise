const app = require("./app");

describe("today", () => {
    it("returns today's formatted date", () => {
        expect(app.today()).toBe(new Date().toLocaleDateString());
    });
});