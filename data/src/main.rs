fn main() {
    let mut rdr =
        csv::Reader::from_path("input_data/meteorological_data/Modified_Output_precip.csv")
            .unwrap();

    let line = rdr.records().next().unwrap().unwrap();

    println!("{:?}", line);
}
