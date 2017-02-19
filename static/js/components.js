class Root extends React.Component {

  constructor(props) {
    super(props);
    this.props = props;
    this.state = { loading: false, results: {}, q: '' };

    this.render = this.render.bind(this);
    this.search = this.search.bind(this);
    this.callback = this.callback.bind(this);
    this.fallback = this.fallback.bind(this);
  }

  search(e) {
    var q = e.target.elements[0].value;
    e.preventDefault();
    e.stopPropagation();
    var config = {
      url: '/api/search/?q=' + encodeURIComponent(q) + '&limit=25',
      method: 'GET',
      success: this.callback,
      error: this.fallback
    };
    $.ajax(config);
    this.setState({ loading: true, q: q });
  }

  callback(json, textStatus, jqXhr) {
    this.setState({ loading: false, results: json });
  }

  fallback(jqXhr, textStatus, error) {
    this.setState({ loading: false });
  }

  render() {
    return React.createElement(
      'div',
      { className: 'container-fluid' },
      React.createElement(
        'header',
        { className: 'header' },
        React.createElement(
          'h2',
          null,
          'T411 Unlocked'
        ),
        React.createElement(
          'small',
          null,
          'Moteur de recherche de torrents anonymis\xE9s, sans pub, opensource.'
        )
      ),
      React.createElement(
        SearchForm,
        { loading: this.state.loading, search: this.search.bind(this), q: this.state.q },
        this.state.results
      )
    );
  }
}

class SearchForm extends React.Component {

  constructor(props) {
    super(props);
    this.props = props;

    this.render = this.render.bind(this);
  }

  render() {
    return React.createElement(
      'div',
      null,
      React.createElement(
        'div',
        { className: 'searchbloc' },
        React.createElement(
          'form',
          { className: 'form', onSubmit: this.props.search },
          React.createElement(
            'label',
            { htmlFor: 'q' },
            'Entrez votre recherche'
          ),
          React.createElement(
            'div',
            { className: 'input-group' },
            React.createElement('input', { type: 'text', className: 'form-control', placeholder: 'Artiste, film, s\xE9rie, jeu...', name: 'q', autofocus: true, required: true, defaultValue: this.props.q }),
            React.createElement(
              'div',
              { className: 'input-group-btn' },
              React.createElement(
                'button',
                { className: 'btn btn-default', type: 'submit' },
                React.createElement('i', { className: this.props.loading ? "fa fa-spinner" : "fa fa-search" })
              )
            )
          )
        )
      ),
      React.createElement(
        'div',
        { className: 'searchbloc nopadding' },
        React.createElement(
          'div',
          { className: 'results' },
          React.createElement(
            ResultTable,
            null,
            this.props.children
          )
        )
      )
    );
  }
}

class ResultTable extends React.Component {

  static parseSize(bytes, precision) {
    var kilobyte = 1024;
    var megabyte = kilobyte * 1024;
    var gigabyte = megabyte * 1024;
    var terabyte = gigabyte * 1024;

    if (bytes >= 0 && bytes < kilobyte) {
      return bytes + ' B';
    } else if (bytes >= kilobyte && bytes < megabyte) {
      return (bytes / kilobyte).toFixed(precision) + ' KB';
    } else if (bytes >= megabyte && bytes < gigabyte) {
      return (bytes / megabyte).toFixed(precision) + ' MB';
    } else if (bytes >= gigabyte && bytes < terabyte) {
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
    for (i = 0; i < this.props.children.torrents.length; i++) {
      t = this.props.children.torrents[i];
      trs.push(React.createElement(
        'tr',
        { className: 'result-item' },
        React.createElement(
          'td',
          { className: 'result-item-name vert-align' },
          React.createElement(
            'a',
            { href: '/api/download/' + t.id + '/' + encodeURIComponent(t.name) + '.torrent' },
            t.name
          ),
          ' ',
          React.createElement(
            'span',
            { className: 'label label-default' },
            t.categoryname
          )
        ),
        React.createElement(
          'td',
          { className: 'result-item-size vert-align alert-info' },
          ResultTable.parseSize(parseInt(t.size))
        ),
        React.createElement(
          'td',
          { className: 'result-item-seeders vert-align alert-success' },
          t.seeders
        ),
        React.createElement(
          'td',
          { className: 'result-item-leechers ver-align alert-danger' },
          t.leechers
        )
      ));
    }
    return React.createElement(
      'div',
      { className: 'table-responsive' },
      React.createElement(
        'table',
        { className: 'table table-striped table-bordered table-hover' },
        React.createElement(
          'thead',
          null,
          React.createElement(
            'tr',
            null,
            React.createElement(
              'th',
              null,
              'Nom'
            ),
            React.createElement(
              'th',
              null,
              'Taille'
            ),
            React.createElement(
              'th',
              null,
              'Seeders'
            ),
            React.createElement(
              'th',
              null,
              'Leechers'
            )
          )
        ),
        React.createElement(
          'tbody',
          null,
          trs
        )
      )
    );
  }
}