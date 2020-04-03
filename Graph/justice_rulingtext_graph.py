# encoding: utf-8

"""
project = zlr
file_name = justice_rulingtext_graph
author = Administrator
datetime = 2020/4/2 0002 下午 15:40
from = office desktop
"""
import datetime as dt
from Graph import BaseGraph
from Calf.data import BaseModel
from Graph.entity import Ruling, RulingText
# from Graph.entity import Enterprise
from Graph.exception import SuccessMessage
from Graph.relationship import Have
# from Graph.enterprise_graph import EtpGraph


class JusRulingTextGraph(BaseGraph):

    def __init__(self):
        BaseGraph.__init__(self)
        self.base = BaseModel(tn='重庆裁决文书(内容)')
        pass

    def create_all_relationship(self):
        """
        1.ruling -[have]->ruling_text
        :return:
        """
        rts = self.base.query(
            sql={'metaModel': '裁判文书'},
            no_cursor_timeout=True)
        i, k = 0, 0
        # eg = EtpGraph()
        etp_count = rts.count()
        relationships = []
        # prs = Person()
        ruling = Ruling()
        for r in rts:
            k += 1
            rt = RulingText.create_from_original_text(
                r['content'], **{'链接': r['url']}
            )
            rl_n = self.NodeMatcher.match(ruling.label).where(
                '_.CASE_NUM="{}"'.format(   # OR _.URL="{}"
                    rt.BaseAttributes['CASE_NUM'],
                    # rt.BaseAttributes['URL']
                )
            ).first()
            if rl_n is None:
                continue
            relationships.append(
                Have(rl_n, rt.get_neo_node(primarykey=rt.primarykey)
                     ).get_relationship()
            )
            if len(relationships) > 100:
                i += 1
                self.graph_merge_relationships(relationships)
                print(SuccessMessage('{}:success merge relationships to database '
                                     'round {} and deal {}/{} enterprise,and'
                                     ' merge {} relationships.'.format(
                    dt.datetime.now(), i, k, etp_count, len(relationships)
                )))
                relationships.clear()
                # return
            pass


# rtg = JusRulingTextGraph()
# rtg.create_all_relationship()