class Root extends React.Component {
  
  constructor(props) {
    super(props);
    this.props = props;
    this.state = {loading: false, results:{}, q:''};

    this.render   = this.render.bind(this);
    this.search   = this.search.bind(this);
    this.callback = this.callback.bind(this);
    this.fallback = this.fallback.bind(this);
  }

  search(e) {
    var q = e.target.elements[0].value;
    e.preventDefault();
    e.stopPropagation();
    var config = {
      url: '/api/search/?q='+encodeURIComponent(q)+'&limit=25',
      method:'GET',
      success: this.callback,
      error: this.fallback
    };
    $.ajax(config);
    this.setState({loading:true, q:q});
  }

  callback(json, textStatus, jqXhr) {
    this.setState({loading:false, results:json});
  }

  fallback(jqXhr, textStatus, error) {
    this.setState({loading:false});
  }

    
  render() {
    return ( 
      <div className="container-fluid">
        <header className="header">
          <h2>T411 Unlocked</h2>
          <small>Moteur de recherche de torrents anonymisés, sans pub, opensource.</small>
        </header>
        <SearchForm loading={this.state.loading} search={this.search.bind(this)} q={this.state.q}>
          {this.state.results}
        </SearchForm>
      </div>
    );
  }
}

class SearchForm extends React.Component {

  constructor(props) {
    super(props);
    this.props = props;

    this.render   = this.render.bind(this);
  }
 
  render() {
    return (
      <div>
        <div className="searchbloc">
          <form className="form" onSubmit={this.props.search}>
            <label htmlFor="q">Entrez votre recherche</label>
            <div className="input-group">
              <input type="text" className="form-control" placeholder="Artiste, film, série, jeu..." name="q" autofocus required defaultValue={this.props.q} />
              <div className="input-group-btn">
                <button className="btn btn-default" type="submit">
                  <i className={this.props.loading?"fa fa-spinner":"fa fa-search"}></i>
                </button>
              </div>
            </div>
          </form>
        </div>
        <div className="searchbloc nopadding">
          <div className="results">
            <ResultTable>{ this.props.children }</ResultTable>
          </div>
        </div>
      </div>
    );
  }
}

class ResultTable extends React.Component {
  
  static parseSize(bytes, precision) {
        var kilobyte = 1024;
        var megabyte = kilobyte * 1024;
        var gigabyte = megabyte * 1024;
        var terabyte = gigabyte * 1024;

        if ((bytes >= 0) && (bytes < kilobyte)) {
            return bytes + ' B';

        } else if ((bytes >= kilobyte) && (bytes < megabyte)) {
            return (bytes / kilobyte).toFixed(precision) + ' KB';

        } else if ((bytes >= megabyte) && (bytes < gigabyte)) {
            return (bytes / megabyte).toFixed(precision) + ' MB';

        } else if ((bytes >= gigabyte) && (bytes < terabyte)) {
            return (bytes / gigabyte).toFixed(precision) + ' GB';

        } else if (bytes >= terabyte) {
            return (bytes / terabyte).toFixed(precision) + ' TB';

        } else {
            return bytes + ' B';
        }
    } 

  render() {
    if (!this.props.children.torrents) return null;

    var trs = [];
    var i, t;
    for(i=0;i<this.props.children.torrents.length;i++) {
      t = this.props.children.torrents[i];
      trs.push(
        <tr className="result-item">
          <td className="result-item-name vert-align">
            <a href={'/api/download/'+t.id+'/'+encodeURIComponent(t.name)+'.torrent'}>{t.name}</a> <span className="label label-default">{t.categoryname}</span>
          </td>
          <td className="result-item-size vert-align alert-info">{ResultTable.parseSize(parseInt(t.size))}</td>
          <td className="result-item-seeders vert-align alert-success">{t.seeders}</td>
          <td className="result-item-leechers ver-align alert-danger">{t.leechers}</td>
        </tr>
      );
    }
    return (
      <div className="table-responsive">
        <table className="table table-striped table-bordered table-hover">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Taille</th>
              <th>Seeders</th>
              <th>Leechers</th>
            </tr>
          </thead>
          <tbody>
          { trs }
          </tbody>
        </table>
      </div>
    );
  }
}
