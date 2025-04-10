#[macro_use] extern crate rocket;
use rocket::serde::json::Json;
use rocket::serde::Serialize;

#[derive(Serialize)]
struct PingResponse {
    message: &'static str,
}

#[get("/ping")]
fn ping() -> Json<PingResponse> {
    Json(PingResponse { message: "pong" })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![ping])
        .configure(rocket::Config {
            address: "0.0.0.0".parse().unwrap(),
            ..rocket::Config::default()
        })
}
