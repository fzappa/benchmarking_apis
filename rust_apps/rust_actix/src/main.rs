use actix_web::{get, web, App, HttpResponse, HttpServer, Responder};
use serde::Serialize;

#[derive(Serialize)]
struct PingResponse {
    message: &'static str,
}

#[get("/ping")]
async fn ping() -> impl Responder {
    let response = PingResponse { message: "pong" };
    HttpResponse::Ok().json(response)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new().service(ping)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}