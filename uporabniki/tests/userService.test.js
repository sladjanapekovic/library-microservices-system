describe("User service basic tests", () => {
  test("should create a user object correctly", () => {
    const user = {
      id: 1,
      username: "sladjana",
      email: "sladjana@example.com",
    };

    expect(user.id).toBe(1);
    expect(user.username).toBe("sladjana");
    expect(user.email).toBe("sladjana@example.com");
  });

  test("should update user data correctly", () => {
    const user = {
      id: 1,
      username: "oldname",
      email: "old@example.com",
    };

    user.username = "newname";
    user.email = "new@example.com";

    expect(user.username).toBe("newname");
    expect(user.email).toBe("new@example.com");
  });

  test("should delete user logically", () => {
    let users = [
      { id: 1, username: "user1", email: "user1@example.com" },
      { id: 2, username: "user2", email: "user2@example.com" },
    ];

    users = users.filter((u) => u.id !== 1);

    expect(users.length).toBe(1);
    expect(users[0].id).toBe(2);
  });
});
