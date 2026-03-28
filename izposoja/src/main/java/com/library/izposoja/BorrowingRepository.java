package com.library.izposoja;

import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import reactor.core.publisher.Flux;

public interface BorrowingRepository extends ReactiveCrudRepository<Borrowing, Long> {

    Flux<Borrowing> findByUserId(Long userId);

}
