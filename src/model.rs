use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct CredsRequest {
    pub email: String,
    pub password: String
}

#[derive(Serialize)]
pub struct Response {
    pub message: String
}

#[derive(Deserialize)]
pub struct FirebaseConfig {
    pub apiKey: String,
    pub authDomain: String,
    pub databaseUrl: String,
    pub projectId: String,
    pub storageBucket: String,
    pub messagingSenderId: String,
    pub appId: String,
}

#[derive(Serialize)]
pub struct AuthResponse {
    pub success: bool,
    pub message: String,
}