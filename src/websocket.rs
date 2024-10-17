use actix::*;
use actix_web::{Error, HttpRequest, HttpResponse, web};
use actix_web_actors::ws;

pub struct MyWebSocket;

impl Actor for MyWebSocket {
    type Context = ws::WebsocketContext<Self>;
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for MyWebSocket {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Text(text)) => {
                ctx.text(text);
            }
            Ok(ws::Message::Binary(bin)) => {
                ctx.binary(bin);
            }
            _ => (),
        }
    }
}

pub async fn ws_index(r: HttpRequest, stream: web::Payload) -> Result<HttpResponse, Error> {
    ws::start(MyWebSocket {}, &r, stream)
}