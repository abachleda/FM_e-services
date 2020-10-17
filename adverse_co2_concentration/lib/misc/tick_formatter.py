# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 12:09:01 2020

@author: ABachleda-Baca
"""
from bokeh.models import TickFormatter
from bokeh.core.properties import Dict, Int, String
from lib.misc.extract_annomalies1 import extract_annomalies1

class FixedTickFormatter(TickFormatter):
    """
    Class used to allow custom axis tick labels on a bokeh chart
    Extends bokeh.model.formatters.TickFormatte
    """

    JS_CODE =  """
        import {Model} from "model"
        import * as p from "core/properties"

        export class FixedTickFormatter extends Model
          type: 'FixedTickFormatter'
          doFormat: (ticks) ->
            labels = @get("labels")
            return (labels[tick] ? "" for tick in ticks)
          @define {
            labels: [ p.Any ]
          }
    """

    labels = Dict(Int, String, help="""
    A mapping of integer ticks values to their labels.
    """)

    __implementation__ = JS_CODE