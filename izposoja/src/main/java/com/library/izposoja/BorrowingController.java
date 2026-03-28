package com.library.izposoja;

import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/borrowings")
public class BorrowingController {

    private final BorrowingRepository repository;
    private final MessageProducer messageProducer;

    public BorrowingController(BorrowingRepository repository, MessageProducer messageProducer) {
        this.repository = repository;
        this.messageProducer = messageProducer;
    }

    // GET all
    @GetMapping
    public Flux<Borrowing> getAllBorrowings() {
        return repository.findAll();
    }

    // GET by ID
    @GetMapping("/{id}")
    public Mono<Borrowing> getBorrowingById(@PathVariable Long id) {
        return repository.findById(id);
    }

    // GET by user
    @GetMapping("/user/{userId}")
    public Flux<Borrowing> getByUser(@PathVariable Long userId) {
        return repository.findByUserId(userId);
    }

    // CREATE borrowing
    @PostMapping
    public Mono<Borrowing> createBorrowing(@RequestBody Borrowing borrowing) {
        borrowing.setBorrowedAt(LocalDateTime.now());
        borrowing.setReturned(false);

        System.out.println("Creating borrowing for user " + borrowing.getUserId());

        return repository.save(borrowing)
                .doOnSuccess(savedBorrowing ->
                        messageProducer.sendBorrowingCreatedMessage(savedBorrowing)
                );
    }

    // RETURN book
    @PutMapping("/{id}/return")
    public Mono<Borrowing> returnBook(@PathVariable Long id) {
        return repository.findById(id)
                .flatMap(b -> {
                    b.setReturned(true);
                    return repository.save(b);
                });
    }

    // DELETE
    @DeleteMapping("/{id}")
    public Mono<Void> deleteBorrowing(@PathVariable Long id) {
        return repository.deleteById(id);
    }
}
