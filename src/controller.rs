use actix_web::{web, HttpResponse, Responder};
use firebase_auth_sdk::FireAuth;
use crate::model::{CredsRequest, AuthResponse};

async fn sign_in(service: web::Data<FireAuth>, creds_request: web::Json<CredsRequest>) -> impl Responder {
    println!("{} {}", creds_request.email, creds_request.password); // Línea que debe ejecutarse

    match service.sign_in_email(&creds_request.email, &creds_request.password, true).await {
        Ok(response) => {
            HttpResponse::Ok().json(AuthResponse {
                success: true,
                message: "Successfully LoggedIn".to_string(),
            })
        }
        Err(ex) => {
            eprintln!("{:?}", ex);
            HttpResponse::Unauthorized().json(AuthResponse {
                success: false,
                message: "Invalid Credentials".to_string(),
            })
        }
    }
}

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/auth")
            .route("/sign_in", web::post().to(sign_in))
    );
}