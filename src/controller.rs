use actix_web::{web, App, HttpServer, HttpResponse, HttpRequest, Result};
use actix_files::Files;
use firebase_auth::{FirebaseAuth, FirebaseUser};
use std::sync::Mutex;

async fn login_page() -> Result<actix_files::NamedFile> {
    Ok(actix_files::NamedFile::open("./static/login.html")?)
}

async fn authenticate(req: HttpRequest, data: web::Data<AppState>) -> HttpResponse {
    // Obtener el token de Firebase del encabezado de autorización
    let auth_header = req.headers().get("Authorization");
    if auth_header.is_none() {
        return HttpResponse::Unauthorized().finish();
    }
    let auth_header = auth_header.unwrap().to_str().unwrap();
    if !auth_header.starts_with("Bearer ") {
        return HttpResponse::Unauthorized().finish();
    }
    let token = &auth_header[7..];


    // #[get("/hello")]
    // async fn greet(user: FirebaseUser) -> impl Responder {
    //     let email = user.email.unwrap_or("empty email".to_string());
    //     format!("Hello {}!", email)
    // }

    // Verificar el token de Firebase
    match data.firebase_auth.verify_id_token(token).await {
        Ok(claims) => {
            // Redirigir a la página de bienvenida con el correo electrónico del usuario
            let email = claims.email.unwrap_or_else(|| "Unknown".to_string());
            HttpResponse::Found()
                .append_header(("Location", format!("/welcome?email={}", email)))
                .finish()
        }
        Err(_) => HttpResponse::Unauthorized().finish(),
    }
}

async fn welcome_page(req: HttpRequest) -> Result<HttpResponse> {
    let query: String = req.query_string().to_string();
    let email = query.split('=').nth(1).unwrap_or("Unknown");
    let content = format!("<h1>Welcome, {}</h1>", email);
    Ok(HttpResponse::Ok().content_type("text/html").body(content))
}

struct AppState {
    firebase_auth: FirebaseAuth,
}

// Usa serde para serializar y deserializar la serviceAccountKey.json

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Cargar la clave de servicio de Firebase desde el archivo serviceAccountKey.json
    let firebase_auth = FirebaseAuth::new("serviceAccountKey.json").await.unwrap();
    let data = web::Data::new(AppState { firebase_auth });

    HttpServer::new(move || {
        App::new()
            .app_data(data.clone())
            .route("/login", web::get().to(login_page))
            .route("/authenticate", web::get().to(authenticate))
            .route("/welcome", web::get().to(welcome_page))
            .service(Files::new("/static", "./static").show_files_listing())
    })
    .bind("")?
    .run()
    .await
}
