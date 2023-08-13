// use diesel::pg::PgConnection;
use diesel::prelude::*;
use diesel::sqlite::SqliteConnection;
use pulldown_cmark::{Event, LinkType, Parser, Tag};
use std::env;
use std::fs::read_to_string;
use walkdir::WalkDir;

fn establish_connection() -> SqliteConnection {
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");

    SqliteConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))

    // PgConnection::establish(&database_url)
    //     .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
}

fn list_md_files(dir: &str) -> impl Iterator<Item = String> + '_ {
    println!("Fetching markdown files from {}", dir);
    WalkDir::new(dir)
        .follow_links(true)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|f| f.file_type().is_file())
        .filter_map(|f| {
            f.path()
                .canonicalize()
                .map(|p| p.to_string_lossy().to_string())
                .ok()
        })
        .filter(|p| p.ends_with(".md"))
}

pub fn extract_links(file: &str) -> Option<Vec<String>> {
    let input: String = read_to_string(file).ok()?;
    Some(
        Parser::new(&input)
            .filter_map(|event| match event {
                Event::Start(tag) => Some(tag),
                _ => None,
            })
            .filter_map(|tag| match tag {
                Tag::Link(LinkType::Inline, link, _) => Some(link),
                _ => None,
            })
            .map(|link| link.to_string())
            .collect(),
    )
}

fn get_raw_content(link: &str) -> Option<String> {
    reqwest::blocking::get(link).ok()?.text().ok()
}

fn main() {
    establish_connection();

    let md_dir = env::var("MD_DIR").expect("MD_DIR must be set");
    let contents = list_md_files(&md_dir)
        .filter_map(|file| extract_links(&file))
        .flatten()
        .filter_map(|l| get_raw_content(&l));

    for content in contents {
        println!("{}", content);
    }

    println!("Hello, world!");
}
