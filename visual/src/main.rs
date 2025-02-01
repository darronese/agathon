use anyhow::Result;

mod conversions;
mod elevations;
mod model;
mod settings;
mod update;
mod view;

fn main() -> Result<()> {
    nannou::app(model::model).update(update::update).run();

    Ok(())
}
