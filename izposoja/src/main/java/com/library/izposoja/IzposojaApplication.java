package com.library.izposoja;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jms.annotation.EnableJms;

@SpringBootApplication
@EnableJms
public class IzposojaApplication {

    public static void main(String[] args) {
        SpringApplication.run(IzposojaApplication.class, args);
    }
}
