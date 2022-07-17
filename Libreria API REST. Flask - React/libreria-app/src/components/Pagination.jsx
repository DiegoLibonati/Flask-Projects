export const Pagination = ({ totalBooks, booksPerPage, paginate }) => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalBooks / booksPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <ul className="pagination_list">
      {pageNumbers.map((number) => (
        <li onClick={() => paginate(number)} key={number * 5478}>
          {number}
        </li>
      ))}
    </ul>
  );
};
