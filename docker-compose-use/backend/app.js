const restful = require("node-restful");
const express = require("express");
const mongoose = restful.mongoose;
const server = express();
const bodyParser = require("body-parser");
const cors = require("cors");

// Database
mongoose.Promise = global.Promise;
mongoose
  .connect("mongodb://db/mydb", {
    useMongoClient: true,
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("MongoDB conectado"))
  .catch((err) => console.error("Erro na conexão com MongoDB:", err));

//Middleware
server.use(bodyParser.urlencoded({ extended: true }));
server.use(bodyParser.json());
server.use(cors());

// ODM
const Client = restful.model("Client", {
  name: { type: String, required: true },
});

// Rest API
Client.methods(['get','post','put','delete'])
Client.updateOptions({new: true, runValidations: true})

// Routes
Client.register(server, '/clients')

// Teste
server.get("/", (req, res) => res.send("Backend"));

// Server
server.listen(3000, () => {
  console.log("Servidor rodando na porta 3000");
});
