import React from 'react';
import WordCloudCard from './wordcloud_card';
import Spinner from 'react-bootstrap/Spinner';
import Masonry from 'react-masonry-component';

import { getClouds } from "./apis";

class WordCloudIndex extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            clouds: null
        };
    }
    componentDidMount() {
        getClouds().then((clouds) => {
            this.setState({clouds: clouds});
        });
    }

    renderCloudCard(cloud) {
        return <WordCloudCard
            id={cloud.id}
            title={cloud.title}
            text={cloud.text}
            created={cloud.updated}
            image={cloud.s3_path}
            key={cloud.id}
        />
    }

    render() {
        if (!this.state.clouds) {
            return (
                <Spinner animation="grow" role="status">
                    <span className="sr-only">Loading...</span>
                </Spinner>
            );
        }
        return (
            <Masonry
                className={'my-gallery-class'} // default ''
                disableImagesLoaded={false} // default false
                updateOnEachImageLoad={false} // default false and works only if disableImagesLoaded is false
            >
                {this.state.clouds.map(cloud => this.renderCloudCard(cloud))}
            </Masonry>
        );
    }
}

export default WordCloudIndex;
