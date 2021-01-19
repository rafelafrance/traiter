"""Build a pipe that retokenizes entity spans into a single token."""
#
# from spacy.language import Language
# from spacy.pipeline import EntityRuler
# from spacy.tokens import Doc
#
# from traiter.patterns_ import PatternRulerType
#
#
# @Language.factory(
#     'retokenize_ruler',
#     default_config={'attr': 'LOWER', 'overwrite': True}
# )
# def retokenize_ruler(
#         nlp: Language,
#         name: str,
#         patterns: PatternRulerType,
#         attr: str,
#         overwrite: bool):
#     """Create a retokenize ruler pipe."""
#     return RetokenizeRulerPipe(nlp, patterns, attr, overwrite)
#
#
# class RetokenizeRulerPipe:
#     """Add an entity ruler that retokenizes matches."""
#
#     def __init__(
#             self,
#             nlp: Language,
#             patterns: PatternRulerType,
#             attr: str = 'lower',
#             overwrite: bool = True
#     ) -> None:
#         self.nlp = nlp
#         self.ruler = EntityRuler(
#             nlp, phrase_matcher_attr=attr, overwrite_ents=overwrite)
#         self.ruler.add_patterns(patterns)
#
#     def __call__(self, doc: Doc) -> Doc:
#         """Find all term in the text and return the resulting doc."""
#         self.ruler(doc)
#         with doc.retokenize() as retokenizer:
#             for ent in doc.ents:
#                 attrs = {'ENT_TYPE': ent.label_, 'ENT_IOB': 3,
#                          '_': {'data': ent._.data, 'label_cache': ent.label_}}
#                 retokenizer.merge(ent, attrs=attrs)
#         return doc
#
#     # @classmethod
#     # def add_pipe(
#     #         cls,
#     #         nlp: Language,
#     #         patterns: Patterns,
#     #         *,
#     #         attr: str = 'lower',
#     #         name: str = 'entity_ruler',
#     #         **kwargs
#     # ) -> None:
#     #     """Add an entity ruler to the pipeline."""
#     #     kwargs = {'before': 'parser'} if not kwargs else kwargs
#     #     ruler = RetokenizeRulerPipe(nlp, patterns.for_ruler(), attr=attr)
#     #     nlp.add_pipe(ruler, name=name, **kwargs)
