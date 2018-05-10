"use strict";

define([], function() {

  function Graph(elementId, data, option) {
    this._elementID = elementId;
    this._data = data;
    this._option = option;
    this._chart = null;
  }

  Graph.prototype.updateGraph = function(newData) {
    this._data = newData;
    this._chart.data.labels = newData.keys;
    this._chart.data.datasets[0].data = newData.values;
    this._chart.update();
  };

  return Graph;
});