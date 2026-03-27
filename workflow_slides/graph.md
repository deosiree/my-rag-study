graph TD;
	__start__([<p>__start__</p>]):::first
	pick_topic(pick_topic)
	as_question(as_question)
	as_fact(as_fact)
	summary(summary)
	__end__([<p>__end__</p>]):::last
	__start__ --> pick_topic;
	as_fact --> summary;
	as_question --> summary;
	pick_topic -.-> as_fact;
	pick_topic -.-> as_question;
	summary --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
