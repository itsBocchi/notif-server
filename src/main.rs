use actix_web::{App, HttpServer, web, middleware::Logger};
use actix_files as fs;
use firebase_auth_sdk::FireAuth;
use std::sync::Arc;
use std::fs::File;
use std::io::Read;
use crate::model::FirebaseConfig;
use log::info;
use log4rs;

mod controller;
mod model;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Inicializar log4rs
    log4rs::init_file("config/log4rs.yaml", Default::default()).unwrap();

    // Log a message to verify logging is working
    info!("Starting the server...");

    // Leer el archivo de configuración
    let mut file = File::open("config/firebase_config.json").expect("Config file not found");
    let mut config_data = String::new();
    file.read_to_string(&mut config_data).expect("Failed to read config file");

    // Parsear el archivo de configuración
    let config: FirebaseConfig = serde_json::from_str(&config_data).expect("Failed to parse config file");

    // Inicializar FireAuth
    let fire_auth = Arc::new(FireAuth::new(config.apiKey));

    // Configurar el servidor Actix-web
    HttpServer::new(move || {
        App::new()
            .wrap(Logger::default())
            .app_data(web::Data::new(fire_auth.clone()))
            .configure(controller::config)
            .service(fs::Files::new("/", "./static").index_file("index.html"))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}