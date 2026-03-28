package com.library.izposoja;

import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Component;

@Component
public class MessageProducer {

    private final JmsTemplate jmsTemplate;

    public MessageProducer(JmsTemplate jmsTemplate) {
        this.jmsTemplate = jmsTemplate;
    }

    public void sendBorrowingCreatedMessage(Borrowing borrowing) {
        String message = "Borrowing created: userId=" + borrowing.getUserId()
                + ", bookId=" + borrowing.getBookId();

        jmsTemplate.convertAndSend("borrowings.queue", message);
        System.out.println("Sent message to ActiveMQ: " + message);
    }
}
