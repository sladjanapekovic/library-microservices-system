const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");
const path = require("path");

const PROTO_PATH = path.join(__dirname, "../proto/user.proto");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});

const userProto = grpc.loadPackageDefinition(packageDefinition).uporabniki;

// Za sada ćemo koristiti privremenu listu korisnika,
// kasnije ćemo to zameniti PostgreSQL bazom.
let users = [];
let currentId = 1;

function createUser(call, callback) {
  const newUser = {
    id: currentId++,
    username: call.request.username,
    email: call.request.email,
  };

  users.push(newUser);
  callback(null, { user: newUser });
}

function getUser(call, callback) {
  const user = users.find((u) => u.id === call.request.id);

  if (!user) {
    return callback({
      code: grpc.status.NOT_FOUND,
      details: "User not found",
    });
  }

  callback(null, { user });
}

function getAllUsers(call, callback) {
  callback(null, { users });
}

function updateUser(call, callback) {
  const user = users.find((u) => u.id === call.request.id);

  if (!user) {
    return callback({
      code: grpc.status.NOT_FOUND,
      details: "User not found",
    });
  }

  user.username = call.request.username;
  user.email = call.request.email;

  callback(null, { user });
}

function deleteUser(call, callback) {
  const index = users.findIndex((u) => u.id === call.request.id);

  if (index === -1) {
    return callback({
      code: grpc.status.NOT_FOUND,
      details: "User not found",
    });
  }

  users.splice(index, 1);
  callback(null, { message: "User deleted successfully" });
}

function main() {
  const server = new grpc.Server();

  server.addService(userProto.UserService.service, {
    CreateUser: createUser,
    GetUser: getUser,
    GetAllUsers: getAllUsers,
    UpdateUser: updateUser,
    DeleteUser: deleteUser,
  });

  const address = "0.0.0.0:50051";

  server.bindAsync(address, grpc.ServerCredentials.createInsecure(), (error, port) => {
    if (error) {
      console.error("Failed to start gRPC server:", error);
      return;
    }

    console.log(`User gRPC server is running on ${address}`);
  });
}

main();
