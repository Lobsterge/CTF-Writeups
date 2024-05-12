use std::{
    include_bytes,
    include_str,
    io::Write,
};

use secrecy::{
    ExposeSecret,
    Secret,
};

const MAX_USERNAME_LENGTH: usize = 32usize;
const MAX_PASSWORD_LENGTH: usize = 32usize;

#[repr(C)]
struct User {
    username_size: usize,
    password_size: usize,
    username: [u8; MAX_USERNAME_LENGTH],
    password: [u8; MAX_PASSWORD_LENGTH],
}

macro_rules! set_field {
    ($self:expr, $value:expr, $max_len:expr, $field_size:ident, $field:ident) => {
        $self.$field_size = $value.len();
        let value_chars = $value.chars().collect::<Vec<_>>();
        if value_chars.len() > $max_len {
            panic!("Value must not exceed {} characters!", $max_len);
        }

        unsafe {
            std::ptr::copy_nonoverlapping(
                $value.as_bytes().as_ptr(),
                $self.$field.as_mut_ptr(),
                value_chars.len(),
            );
        }
    };
}

impl User {
    fn empty() -> Self {
        Self {
            username_size: 0usize,
            password_size: 0usize,
            username: [0u8; MAX_USERNAME_LENGTH],
            password: [0u8; MAX_PASSWORD_LENGTH],
        }
    }

    fn set_username(&mut self, username: &str) {
        set_field!(self, username, MAX_USERNAME_LENGTH, username_size, username);
    }

    fn set_password(&mut self, password: &str) {
        set_field!(self, password, MAX_PASSWORD_LENGTH, password_size, password);
    }

    fn print_username(&self) -> () {
        for i in 0..self.username_size {
            unsafe {
                let current_byte = *self.username.get_unchecked(i);
                std::io::stdout()
                    .write_all(&[current_byte])
                    .expect("Error while printing the username");
            }
        }
    }

    fn is_admin(&self, admin_password: Secret<[u8; MAX_PASSWORD_LENGTH]>) -> bool {
        self.password == *admin_password.expose_secret()
    }
}

fn main() {
    let mut user = User::empty();
    let admin_password: Secret<[u8; 32]> =
        Secret::new(*include_bytes!("resources/admin_password.txt"));

    let read_input = |prompt: &str| -> String {
        print!("{}", prompt);
        std::io::stdout().flush().unwrap();

        let mut input = String::new();
        std::io::stdin()
            .read_line(&mut input)
            .expect("Error while reading input");
        input.trim().to_string()
    };

    let username = read_input("Enter your username: ");
    user.set_username(&username);

    print!("Hello, ");
    user.print_username();
    println!("!");

    let password = read_input("Enter password: ");
    user.set_password(&password);

    println!("Here is your flag: ");
    if user.is_admin(admin_password) {
        println!("{}", include_str!("resources/flag.txt"))
    } else {
        println!("{}", include_str!("resources/flag_art.txt"))
    }

    std::io::stdout().flush().unwrap();
}
