mod controller;
mod websocket;

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    server::start_server().await
}