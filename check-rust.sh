#!/bin/sh
echo "fmt:"
cargo fmt -- --check
echo "clippy:"
cargo clippy -q --no-deps -- -D warnings
#echo "build:"
#cargo build -q --release
