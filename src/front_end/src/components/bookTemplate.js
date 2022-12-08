import React from 'react';

/**
 * 
 * @param {Object} results object that holds BookTemplate information
 * @returns html code of BookTemplate
 */
const BookTemplate = ({results}) => {
  if (!results){
    return null
  }
  return  (
    <div>
      {results.map((item) => {
        return (
          <div className='BookTemplate-info' key={item.book_id}>
            <table>
              <tbody>
                <tr>
                  <th>Title</th>
                  <td>{item.title}</td>
                </tr>
                <tr>
                  <th>book_url</th>
                  <td><a href={item.book_url}>{item.book_url}</a></td>
                </tr>
                <tr>
                  <th>Author</th>
                  <td><a href={item.author_url}>{item.author}</a></td>
                </tr>
                <tr>
                  <th>Rating</th>
                  <td>{item.rating}</td>
                </tr>
                {
                  item.similar_books.map((book,index)=>{
                    if (index===0) {
                      return (<tr key={index}>
                        <th>Similar Books</th>
                        <td>{book}</td>
                      </tr>);
                    } else {
                      return (<tr key={index}>
                        <th></th>
                        <td>{book}</td>
                      </tr>);
                    }
                  })
                }
              </tbody>
            </table>
          <img src={item.image_url} alt='book'/>
          </div>
        );
      })}
    </div>
  );}


export default BookTemplate;