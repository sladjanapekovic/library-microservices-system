const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

const { pool, initializeDatabase } = require("./db");

const PROTO_PATH = path.join(__dirname, "../proto/user.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).uporabniki;

// CREATE
async function createUser(call, callback) {
  try {
    const { username, email } = call.request;

    const result = await pool.query(
      "INSERT INTO users (username, email) VALUES ($1, $2) RETURNING *",
      [username, email]
    );

    callback(null, { user: result.rows[0] });
  } catch (err) {
    console.error(err);
    callback(err);
  }
}

// GET ONE
async function getUser(call, callback) {
  try {
    const result = await pool.query(
      "SELECT * FROM users WHERE id = $1",
      [call.request.id]
    );

    if (result.rows.length === 0) {
      return callback({
        code: grpc.status.NOT_FOUND,
        details: "User not found",
      });
    }

    callback(null, { user: result.rows[0] });
  } catch (err) {
    console.error(err);
    callback(err);
  }
}

// GET ALL
async function getAllUsers(call, callback) {
  try {
    const result = await pool.query("SELECT * FROM users");

    callback(null, { users: result.rows });
  } catch (err) {
    console.error(err);
    callback(err);
  }
}

// UPDATE
async function updateUser(call, callback) {
  try {
    const { id, username, email } = call.request;

    const result = await pool.query(
      "UPDATE users SET username = $1, email = $2 WHERE id = $3 RETURNING *",
      [username, email, id]
    );

    if (result.rows.length === 0) {
      return callback({
        code: grpc.status.NOT_FOUND,
        details: "User not found",
      });
    }

    callback(null, { user: result.rows[0] });
  } catch (err) {
    console.error(err);
    callback(err);
  }
}

// DELETE
async function deleteUser(call, callback) {
  try {
    const result = await pool.query(
      "DELETE FROM users WHERE id = $1 RETURNING *",
      [call.request.id]
    );

    if (result.rows.length === 0) {
      return callback({
        code: grpc.status.NOT_FOUND,
        details: "User not found",
      });
    }

    callback(null, { message: "User deleted successfully" });
  } catch (err) {
    console.error(err);
    callback(err);
  }
}

async function main() {
  await initializeDatabase();

  const server = new grpc.Server();

  server.addService(userProto.UserService.service, {
    CreateUser: createUser,
    GetUser: getUser,
    GetAllUsers: getAllUsers,
    UpdateUser: updateUser,
    DeleteUser: deleteUser,
  });

  const address = "0.0.0.0:50051";

  server.bindAsync(address, grpc.ServerCredentials.createInsecure(), (error) => {
    if (error) {
      console.error("Failed to start gRPC server:", error);
      return;
    }

    console.log(`User gRPC server is running on ${address}`);
  });
}

main();
