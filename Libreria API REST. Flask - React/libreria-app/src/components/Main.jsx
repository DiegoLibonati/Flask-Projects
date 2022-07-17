import React, { useState } from "react";
import "../css/config.css";
import "../css/books_container.css";
import "../css/pagination_container.css";
import { useGetBooks } from "../hooks/useGetBooks";
import { Book } from "./Book";
import { FilterItem } from "./FilterItem";
import { useHide } from "../hooks/useHide";
import { AddBook } from "./AddBook";
import { useGetGeneros } from "../hooks/useGetGeneros";
import { Pagination } from "./Pagination";
import { FilterMenu } from "./FilterMenu";

export const Main = () => {
  const { loading, books, defaultFetch, setBooks } = useGetBooks();
  const { hide, handleHide } = useHide();
  const { genero, setGenero } = useGetGeneros();
  const [currentPage, setCurrentPage] = useState(1);
  const [booksPerPage] = useState(7);

  const indexOfLastBook = currentPage * booksPerPage;
  const indexOfFirstBook = indexOfLastBook - booksPerPage;
  const currentBooks = books.slice(indexOfFirstBook, indexOfLastBook);

  if (loading) {
    return <h2>Loading</h2>;
  } else {
    return (
      <>
        <main className="main_container">
          <section className="config_container">
            <article className="filter_genero_container">
              <button onClick={() => handleHide()}>Filters</button>

              {hide ? (
                <ul className="filter_genero_container_list">
                  <li onClick={() => setBooks(defaultFetch)}>Show All</li>
                  <FilterMenu
                    genero={genero}
                    setBooks={setBooks}
                    filterName="Genero"
                  ></FilterMenu>
                </ul>
              ) : (
                <></>
              )}
            </article>
          </section>

          <section className="books_container">
            {currentBooks.map((book) => (
              <Book key={book._id.$oid} {...book}></Book>
            ))}

            <AddBook
              setBooks={setBooks}
              books={books}
              genero={genero}
              setGenero={setGenero}
            ></AddBook>
          </section>

          <section className="pagination_container">
            <Pagination
              booksPerPage={booksPerPage}
              totalBooks={books.length}
              paginate={setCurrentPage}
            ></Pagination>
          </section>
        </main>
      </>
    );
  }
};
