package com.library.izposoja;

import org.springframework.jms.annotation.JmsListener;
import org.springframework.stereotype.Component;

@Component
public class MessageListener {

    @JmsListener(destination = "borrowings.queue")
    public void receiveMessage(String message) {
        System.out.println("Received message from ActiveMQ: " + message);
    }
}
