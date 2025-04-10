use axum::{routing::get, Router, Json};
use serde::Serialize;
use std::net::SocketAddr;
use tracing_subscriber;

#[derive(Serialize)]
struct PingResponse {
    message: &'static str,
}

async fn ping() -> Json<PingResponse> {
    Json(PingResponse { message: "pong" })
}

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();
    let app = Router::new().route("/ping", get(ping));
    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    println!("Listening on {}", addr);
    axum::Server::bind(&addr).serve(app.into_make_service()).await.unwrap();
}