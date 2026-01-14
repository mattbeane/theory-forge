"""
Exemplar Database - Reference paper excerpts for style guidance.

Contains curated excerpts from published papers that demonstrate the target
style for each section type. These are injected into generation prompts to
keep the model in-genre.

NOTE: These exemplars are from qual-forward papers. For quant-forward papers,
the quantitative presentation can be more prominent, but voice, contribution
framing, and theoretical apparatus should still match this register.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Exemplar:
    """A reference excerpt demonstrating target style."""
    source: str          # Paper title/author
    section: str         # Section type
    text: str            # The excerpt
    notes: str           # What this exemplifies
    is_qual_forward: bool = True  # Whether from qual-forward paper


class ExemplarDB:
    """
    Database of reference paper excerpts organized by section.

    Usage:
        db = ExemplarDB()
        exemplar = db.get("introduction")
        prompt = f"Write in this style:\n\n{exemplar.text}"
    """

    def __init__(self):
        self._exemplars = self._build_exemplars()

    def get(self, section: str, prefer_quant: bool = False) -> Optional[Exemplar]:
        """Get exemplar for a section type."""
        key = section.lower().replace(" ", "_")
        return self._exemplars.get(key)

    def get_all(self, section: str) -> list[Exemplar]:
        """Get all exemplars for a section type."""
        key = section.lower().replace(" ", "_")
        exemplar = self._exemplars.get(key)
        return [exemplar] if exemplar else []

    def _build_exemplars(self) -> dict[str, Exemplar]:
        """Build the exemplar database."""
        return {
            "abstract": self._abstract_exemplar(),
            "introduction": self._introduction_exemplar(),
            "introduction_cold_open": self._introduction_cold_open_exemplar(),
            "theory": self._theory_exemplar(),
            "methods": self._methods_exemplar(),
            "iterative_methods": self._iterative_methods_exemplar(),
            "findings": self._findings_exemplar(),
            "findings_quote_integration": self._findings_quote_exemplar(),
            "discussion": self._discussion_exemplar(),
            "contribution": self._contribution_exemplar(),
        }

    def _abstract_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ)",
            section="abstract",
            text="""How do trainees in a community of practice learn new techniques and technologies when approved practices for learning are insufficient? I explore this question through two studies: a two-year, five-sited, comparative, ethnographic study of learning in robotic and traditional surgical practice, and a blinded interview-based study of surgical learning practices at 13 top-tier teaching hospitals around the United States. I found that learning surgery through increasing participation using approved methods worked well in traditional (open) surgery, as current literature would predict. But, the radically different practice of robotic surgery greatly limited trainees' role in the work, making approved methods ineffective. Learning surgery in this context required what I call "shadow learning": an interconnected set of norm- and policy-challenging practices enacted extensively, opportunistically, and in relative isolation that allowed a minority of robotic surgical trainees to come to competence.""",
            notes="""
Key features:
- Opens with research question
- States method concisely
- Names the core concept/contribution ("shadow learning")
- Active voice throughout ("I explore", "I found")
- No bullet points or lists
""",
        )

    def _introduction_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ)",
            section="introduction",
            text="""We have known for decades that the world of work is changing, and communities of practice must cultivate new skills in order to stay relevant. New business models, collaborative practices and technologies all demand new ways of interpreting and acting skillfully in the midst of a new and shifting set of problems, and those communities that do not adapt to these conditions deliver less value and lose jurisdiction. Though this adaptation occurs at the team and organizational levels, communities of practice cannot accomplish it without ensuring an adequate supply of new members capable of performing the work that a changing world requires.

But communities of practice face a dilemma here. Much consequential learning occurs through direct and increasing participation in experts' work, yet such involvement often comes at a cost to experts' quality output. Prioritizing trainee involvement risks increased costs and decreased quality in the short run as trainees consume resources and make errors, and prioritizing output invokes these same risks in the longer term via a shrinking pool of competent members.

So what do trainees do to learn to perform their work in spite of these barriers? Available research on learning in communities of practice focuses elsewhere, in particular on situations in which trainees enjoy 'legitimate peripheral participation' in experts' work – semi-structured and increasing collaboration with experts on real problems involving significant risk, granted via a publically approved role.""",
            notes="""
Key features:
- Opens with theoretical/conceptual claim, not empirical puzzle
- Builds tension gradually
- Uses rhetorical question as pivot ("So what do trainees do...")
- No hypothesis statements
- Active voice, direct claims
- Flows as narrative, no bullets
""",
        )

    def _introduction_cold_open_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Synthetic example based on Wait and See draft",
            section="introduction_cold_open",
            text=""""Telling them now that you got robotics here, they'll all leave."

This prediction—offered by a warehouse operations manager anticipating worker response to automation—reflects conventional wisdom. Workers facing technological displacement should flee to preserve their livelihoods. Yet in six facilities implementing AI-enabled robotics, we observed the opposite: voluntary turnover dropped sharply as automation approached, and workers who stayed performed better than those who left.

This paper explains why conventional wisdom proved wrong.""",
            notes="""
Key features of cold open:
- Quote alone, no setup (ONLY permitted at paper opening or section opening)
- Quote encapsulates the core puzzle
- Immediate analytical framing (within 2 sentences)
- Quote is colorful/voicey ("you got robotics here")
- Transitions quickly to "this paper" statement
""",
        )

    def _theory_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ)",
            section="theory",
            text="""Communities of practice cannot persist without training new members. Competent membership allows them to tackle complex, dynamic problems, expand jurisdiction over those problems and maintain a strong identity and culture. Research has shown that while formal training has an important role to play in this competence, much consequential learning occurs through legitimized peripheral participation in the work core of the community. Legitimated access lets trainees "get it" by "being there" with old hands during the work, and helping out on risky tasks in ways that bring them close to the edge of their expertise.

While on this view individuals may cognitively acquire portable skills, related studies have focused overwhelmingly on learning as a social process. Regardless, the trouble here for trainees and the communities they aspire to join is that economic and efficiency pressures, coupled with technologies that allow experts to perform more of the work without assistance often mean dividing the work such that trainees get less meaningful exposure to experts in action.

Studies of learning in communities of practice have not focused on this problem; they have rather treated legitimate peripheral participation as a given. The socialization literature is an exemplar. Van Maanen shows that once police recruits emerged from the academy, all expected them to go "on the beat" with more senior cops where they would really "learn the ropes." This was an essential and legitimized semi-structured partnership in which they drove their own learning as they helped their more senior counterpart with failure-intolerant policing.""",
            notes="""
Key features:
- Extended engagement with existing literature
- Dialogue with prior work (names scholars, engages their arguments)
- Identifies what prior work assumes/takes for granted
- Builds toward gap identification gradually
- No numbered hypotheses
- Propositions emerge from reasoning, not stated as H1, H2
""",
        )

    def _methods_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ)",
            section="methods",
            text="""My ethnographic work involved site visits and observation of surgical work in the OR nearly every week at five hospitals from 2013 to 2015, as well as recurrent formal and informal interviews with hospital staff. Specifically, this study draws upon 4772 pages of data gathered during 94 surgical procedures, encompassing 478 hours of direct observation. I took time-stamped notes documenting staff interactions and the flow of work before, during and after each procedure, noting technology configuration and use and the roles and responsibilities of each participant.

I further engaged in participant observation, regularly helping with scutwork in the OR (e.g., dealing with trash, running for supplies, turning lights on and off, helping people scrub in), training on a daVinci simulator for six sessions, getting trained to move the robot's arms around for sterile draping, and sitting in the trainee console during procedures.

In order to sample heavily on relatively rare "successful learners", I launched study two, a "blinded snowball" interview study across 13 additional world-renowned teaching institutions throughout the United States. Each AP I interviewed at my ethnographic sites supplied two sets of interview subjects: two or more colleagues with comparable experience and roles at other institutions and two residents from their own institution.""",
            notes="""
Key features:
- First person ("My ethnographic work")
- Emphasizes access and embeddedness
- Narrative rather than procedural
- Concrete details about being there
- Sample description woven into narrative
""",
        )

    def _iterative_methods_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Beane 2023 ASQ (Resourcing a Technological Portfolio)",
            section="iterative_methods",
            text="""I carried out two interdependent and iterative analytical streams: one qualitative, one quantitative. Initial qualitative analysis revealed that robotic surgical work demanded constant coordination between surgeons, residents, and nurses—coordination that shifted dramatically as uncertainty declined. I then turned to quantitative data to identify when these shifts occurred, discovering distinct phases marked by declining variability in procedure length, complication rates, and engineer intervention frequency. These quantitative markers drove me back to qualitative data to understand what had changed organizationally in each phase. The phase structure presented in findings emerged from this iterative process: phases correspond to organizational events informants described as marking qualitative shifts in their work, corroborated by quantitative discontinuities in operational patterns.""",
            notes="""
Key features of iterative methods description:
- Explicitly names "two interdependent and iterative analytical streams"
- Describes puzzle emerging from one data source
- Describes returning to other data source to investigate
- States that framework "emerged from this iterative process"
- Connects qual and quant: qual revealed patterns, quant identified timing, qual explained meaning
- Emphasizes that phases "correspond to organizational events" (qual) "corroborated by quantitative discontinuities" (quant)
""",
            is_qual_forward=True,
        )

    def _findings_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Synthetic example for quant-forward papers",
            section="findings",
            text="""Voluntary resignations decline sharply as automation approaches. In the six months before robot implementation, resignation rates dropped by 18-19 percentage points relative to comparable periods at non-implementing facilities—a pattern that contradicts standard predictions about worker flight from technological displacement.

Table 2 presents the full results. The coefficient on the interaction between proximity to automation and seasonal worker status is substantial and precisely estimated (β = -0.19, SE = 0.03, p < 0.001). This finding reveals that the workers most exposed to automation risk respond by staying, not leaving.

The qualitative evidence illuminates why. Managers described a shift in worker behavior as implementation approached. As one operations director explained:

"Once they knew robots were coming, everything changed. The ones who wanted to prove themselves—they started showing up early, asking for extra shifts. It was like they were auditioning."

This "auditioning" dynamic—workers intensifying effort to signal their value—was particularly pronounced among seasonal workers, who faced the greatest uncertainty about their post-automation prospects.""",
            notes="""
Key features for quant-forward findings:
- Lead with the substantive finding, not the test
- Statistical results followed by "This finding reveals..."
- Quantitative pattern stated, then mechanism illuminated via qual
- Quote preceded by analytical claim
- Quote is colorful ("auditioning")
- Integration of quant and qual in service of single argument
""",
        )

    def _findings_quote_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ) / Developmental Uncertainty draft",
            section="findings_quote_integration",
            text="""Engineers genuinely could not proceed without driver input during this period. The system lacked adequate observability—engineers could not see what was happening in production. As one engineer explained:

"So when we just launched at [first large customer], we had a very 'baby's first day' system. We whiteboarded [it] in an hour or two, then built it the next week, right? So the kind of observability you can get is pretty weak."

Drivers became the primary source of real-time operational intelligence. Engineers recognized them as "that first line of defense and eyes" for the system. Hardware failure identification exemplified this dynamic. Engineers could not observe production-floor realities from their desks, but drivers could:

"[As a driver] you start seeing failures as far as maybe grippers. Whereas the part that attaches the gripper to the arm or something like that starts to break often and we don't really know why. And they [drivers] can point out like, 'Oh well, it's weirdly in this orientation. It's hitting this, and it's sweeping across the bin and hitting other items.'"

The pattern was clear: engineers genuinely did not know what was wrong. Drivers had eyes on problems engineers could not see.""",
            notes="""
Key features of quote integration:
- Analytical claim precedes quote
- Quote is voicey ("baby's first day system", "weirdly in this orientation")
- Analysis continues after quote
- Quote is trimmed to essential content
- Multiple quotes in sequence, each with setup
- Returns to analytical frame after quotes
""",
        )

    def _discussion_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Shadow Learning (Beane, ASQ)",
            section="discussion",
            text="""This study expands our conceptions of learning in communities of practice by showing that when technological change to core methods allows experts to work with less help, successful trainees may learn through shadow learning. And, unlike known learning practices that function through gradually increasing participation in the work, robust participation given such technical change can be starkly dependent on immediate demonstrations of relatively advanced competence that can only be acquired through norm and policy-challenging practices.

The learning literature has traditionally treated legitimate peripheral participation as a given—trainees gain access to increasing involvement in experts' work through an approved role. This research reveals what happens when that assumption fails. When efficiency pressures and technological reconfiguration prevent such participation, a new dynamic emerges: learning moves into the shadows, becoming opportunistic, isolated, and dependent on practices that run counter to stated norms and policies.

Several unintended consequences followed from this mode of learning. First, it led to a star-pupil-take-all dynamic—successful learners gained discrete, increasing and disproportionate access to learning opportunities. Second, those trainees who did engage in shadow learning became hyperspecialized in a world that has room for only a handful of such hyperspecialists.""",
            notes="""
Key features:
- Opens with contribution claim as prose
- Explicitly extends prior theory
- Names the theoretical contribution
- Discusses implications narratively
- NO "three contributions" list
- NO bullet points
""",
        )

    def _contribution_exemplar(self) -> Exemplar:
        return Exemplar(
            source="Multiple reference papers",
            section="contribution",
            text="""This research extends person-environment fit theory by identifying work orientation as a moderator of the misfit-response relationship. Standard P-E fit theory predicts that misfit leads to withdrawal: reduced effort, lower commitment, and exit. This prediction has strong empirical support and captures an important dynamic. But it is incomplete.

We show that when advancement pathways exist, career-oriented workers respond to misfit by intensifying effort rather than withdrawing. Misfit creates motivation to change one's situation; effort creates opportunities to change it. The standard P-E fit prediction holds for job-oriented workers—they don't intensify effort because they aren't seeking advancement. But for career-oriented workers, misfit can motivate.

This contribution connects two literatures that have developed largely in parallel. Work orientation research has established that workers differ in what they want from work, but has not systematically examined how orientation shapes responses to misfit. P-E fit research has documented consequences of misfit but has not incorporated orientation as a moderator. By combining these insights, we identify conditions under which the standard P-E fit prediction inverts.""",
            notes="""
CRITICAL: Contributions as narrative, NEVER as list.

Bad: "Our study makes three contributions. First, we extend... Second, we show... Third, we document..."

Good: "This research extends X by... We show that... This contribution connects..."

The contribution should read as joining a scholarly conversation, not checking boxes.
""",
        )


# Pre-built database instance
EXEMPLAR_DB = ExemplarDB()


def get_exemplar(section: str) -> Optional[Exemplar]:
    """Convenience function to get exemplar for a section."""
    return EXEMPLAR_DB.get(section)


def get_section_prompt_with_exemplar(section: str) -> str:
    """
    Generate a prompt snippet with exemplar for a section.

    Returns text that can be injected into a generation prompt.
    """
    exemplar = EXEMPLAR_DB.get(section)
    if not exemplar:
        return ""

    return f"""
## Style Exemplar

The following excerpt demonstrates the target style for this section.
Match this register, voice, and structure (but not content).

SOURCE: {exemplar.source}

---
{exemplar.text}
---

WHAT THIS EXEMPLIFIES:
{exemplar.notes}
"""
