package com.library.izposoja;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.time.LocalDateTime;

public class BorrowingTest {

    @Test
    void testBorrowingCreation() {
        Borrowing borrowing = new Borrowing(
                1L,
                2L,
                3L,
                LocalDateTime.now(),
                false
        );

        assertNotNull(borrowing);
        assertEquals(2L, borrowing.getUserId());
        assertEquals(3L, borrowing.getBookId());
        assertFalse(borrowing.getReturned());
    }

    @Test
    void testReturnBook() {
        Borrowing borrowing = new Borrowing(
                1L,
                2L,
                3L,
                LocalDateTime.now(),
                false
        );

        borrowing.setReturned(true);

        assertTrue(borrowing.getReturned());
    }
}
