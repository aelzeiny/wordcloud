import React from 'react';
import './App.css';
import WordCloudIndex from './wordcloud_index';
import AddForm from './wordcloud_add';

function App() {
  return (
    <div className="App">
        <WordCloudIndex/>
        <AddForm/>
    </div>
  );
}

export default App;
