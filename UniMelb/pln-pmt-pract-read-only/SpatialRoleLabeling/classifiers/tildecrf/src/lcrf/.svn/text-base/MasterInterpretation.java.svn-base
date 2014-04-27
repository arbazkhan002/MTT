/**
 * 
 */
package lcrf;

import java.io.File;
import java.util.List;

import lcrf.counting.LogicalCountingTreeTrainer;
import lcrf.logic.Atom;
import lcrf.logic.Constant;
import lcrf.logic.Interpretation;
import lcrf.logic.TermSchema;
import lcrf.logic.parser.ParseException;
import lcrf.regression.InterpretationRegressionTreeTrainerBestFirst;
import lcrf.regression.RegressionModelTrainer;
import lcrf.regression.TrainerWrapper;
import lcrf.stuff.Pair;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.PosixParser;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

/**
 * @author Bernd Gutmann
 */
public class MasterInterpretation {
    /**
     * This if the filename for the logging properties of log4j. If it is found
     * in the current path at programm start the properties are read from them
     * otherwise the BasicConfigurator is used. See <a
     * href="http://logging.apache.org/log4j/docs/index.html">log4j</a>
     */
    private static final String PROPERTYFILE = "logging.prop";

    private static final String MODETAGGING = "tagging";

    private static final String MODECLASSIFICATION = "classification";

    private static final String MODECLASSIFICATIONOAA = "classificationoaa";

    private static final String MODECCLASSIFICATIONRR = "classificationrr";

    /**
     * @return
     */
    public static Options getOptions() {
        Options options = new Options();

        options.addOption(OptionBuilder.withArgName("atom3=filename").hasArgs().withLongOpt("data")
                .withDescription("source files for the data (if used n-fold cross validation)").create());

        options.addOption(OptionBuilder.withArgName("atom=filename").hasArgs().withLongOpt("train")
                .withDescription(
                        "source files for the training data (if specified test and training data separatly)")
                .create());

        options.addOption(OptionBuilder.withArgName("atom2=filename").hasArgs().withLongOpt("test")
                .withDescription(
                        "source files for the test data (if specified test and training data separatly)")
                .create());
        
        options.addOption(OptionBuilder.withArgName("atom2=filename").hasArgs().withLongOpt("validation")
                .withDescription(
                        "source files for the validation data")
                .create());
        
        options.addOption(OptionBuilder.hasArg().withLongOpt("improvements").withDescription(
        "train until no improvement of the log-likelihood on the validation set is made since n steps").create());
        
        

        options.addOption(OptionBuilder.hasArg().withLongOpt("folds").withDescription(
                "number of folds for n-fold cross validation").create());

        options.addOption(OptionBuilder.hasArg().withLongOpt("fold").withDescription(
                "number of the fold used for testing in n-fold cross validation").create());

        options.addOption(OptionBuilder.hasArg().withLongOpt("mode").isRequired().withDescription(
                "operation mode, possible values are: " + MasterInterpretation.MODETAGGING + ", "
                        + MasterInterpretation.MODECLASSIFICATION + ", " + MasterInterpretation.MODECLASSIFICATIONOAA + ", "
                        + MasterInterpretation.MODECCLASSIFICATIONRR).isRequired().create('m'));

        options.addOption(OptionBuilder.withDescription(
                "maximal number of training iterations of the CRF (default 5)").hasArg().withArgName("trainsteps")
                .create("n"));
        options.addOption(OptionBuilder.withDescription("window size (default 5").hasArg().withArgName(
                "window size").create("w"));
        options.addOption(OptionBuilder.withDescription("random seed (default 2342666").hasArg().create("r"));

        options.addOption(OptionBuilder.withDescription("minimum leaf size (default=10)").hasArg()
                .create("l"));// FIXME
        options.addOption(OptionBuilder.withDescription("maximum tree depth (default=7)").hasArg()
                .create("d"));
        options.addOption(OptionBuilder.withDescription("schemafile").hasArg().create("s"));
        options.addOption(OptionBuilder.withDescription(
                "Sized of the subsample used for training the regression model (default all)").hasArg()
                .create("x"));
        options.addOption(OptionBuilder.withDescription("Increasement of the subsample size (default 100)")
                .hasArg().create("y"));
        options.addOption(OptionBuilder.withDescription("Increase subsample size after n steps (default 2)")
                .hasArg().create("z"));
        options.addOption(OptionBuilder.withDescription("File with Prolog backgroundknowledge").hasArg()
                .create("b"));

        options.addOption("h", "help", false, "show help");
        return options;
    }

    /**
     * @param args
     * @return
     */
    private static CommandLine parseArguments(String[] args) {
        try {
            return (new PosixParser()).parse(getOptions(), args);
        } catch (org.apache.commons.cli.ParseException e) {
            showHelp(e.getMessage());
            System.exit(1);
        }
        return null;
    }

    /**
     * @param logger
     * @param entries
     * @return
     */
    private static InterpretationExampleContainer processTaggingExamples(Logger logger, String[] entries) {
        InterpretationExampleContainer allExamplesTagging = null;

        for (String entry : entries) {
            logger.info("Read tagging examples from file " + entry);
            InterpretationExampleContainer tmp = XMLInput.readInterpreationExamplesDOM(entry);
            logger.info("Read " + tmp);

            if (allExamplesTagging == null) {
                allExamplesTagging = tmp;
            } else {
                allExamplesTagging.addExamples(tmp);
            }
        }
        return allExamplesTagging;

    }

    /**
     * @param logger
     * @param entries
     * @return
     */
    private static ClassificationExampleContainer processClassificationExamples(Logger logger,
            String[] entries) {
        ClassificationExampleContainer allExamplesClassification = new ClassificationExampleContainer();
        for (String entry : entries) {
            String[] parts = entry.split("=");

            if (parts == null || parts.length != 2 || parts[0].equals("") || parts[1].equals("")) {
                showHelp("entries must have the form atom=filename, " + entry + " is illegal");
                System.exit(1);
            }

            Atom a = null;
            try {
                a = new Atom(parts[0]);
            } catch (ParseException e) {
                showHelp("entries must have the form atom=filename, " + entry + " is illegal because "
                        + parts[0] + " is not a legal atom symbol");
                System.exit(1);
            }

            logger.info("Read classification examples for atom " + a + " from file " + parts[1]);
            Pair<List<List<Atom>>,List<String>> sequences = XMLInput.readSequencesDOM(parts[1]);
            
            allExamplesClassification.addExamples(sequences.o1, a, sequences.o2);            
            logger.info("Read " + sequences.o1.size() + " sequences");

        }

        return allExamplesClassification;
    }

    public static void main(String[] args) {
        // parse the command line
        CommandLine line = parseArguments(args);

        // should we display the help
        if (line.hasOption('h')) {
            showHelp(null);
            System.exit(0);
        }

        Logger optionLogger = Logger.getLogger("main.options");
        Logger preparationLogger = Logger.getLogger("main.preparation");

        if ((new File(MasterInterpretation.PROPERTYFILE)).exists()) {
            PropertyConfigurator.configure(MasterInterpretation.PROPERTYFILE);
        } else {
            BasicConfigurator.configure();
        }

        // which mode
        String mode = line.getOptionValue('m').toLowerCase().trim();
        if (!(mode.equals(MasterInterpretation.MODETAGGING) || mode.equals(MasterInterpretation.MODECLASSIFICATION)
                || mode.equals(MasterInterpretation.MODECLASSIFICATIONOAA) || mode.equals(MasterInterpretation.MODECCLASSIFICATIONRR))) {
            showHelp("Unknown mode: \"" + line.getOptionValue('m') + "\"");
            System.exit(1);
        }

        optionLogger.info("mode is " + mode);

        // read minor parameter
        int crftrainsteps = Integer.parseInt(line.getOptionValue("n", "5"));
        int windowSize = Integer.parseInt(line.getOptionValue("w", "5"));
        int folds = Integer.parseInt(line.getOptionValue("folds", "10"));
        int fold = Integer.parseInt(line.getOptionValue("fold", "0"));
        int treedepth = Integer.parseInt(line.getOptionValue("d", "7"));
        int minleafsize = Integer.parseInt(line.getOptionValue("l", "10"));
        long seed = Long.parseLong(line.getOptionValue("r", "2342666"));
        int subsamplesize = Integer.parseInt(line.getOptionValue("x", "0"));
        int subsampleincreasement = Integer.parseInt(line.getOptionValue("y", "100"));
        int subsampleincreaseafter = Integer.parseInt(line.getOptionValue("z", "2"));
        int improvements = Integer.parseInt(line.getOptionValue("improvements", Integer.toString(crftrainsteps)));
        String schemaFile = line.getOptionValue("s", null);
        String backgroundknowledgeFile = line.getOptionValue("b", null);

        optionLogger.info("General parameters");
        optionLogger.info("folds         : " + folds);
        optionLogger.info("testfoldnr    : " + fold);
        optionLogger.info("mode          : " + mode);

        optionLogger.info("seed          : " + seed);

        optionLogger.info("Regression model parameters");
        optionLogger.info("treedepth     : " + treedepth);
        optionLogger.info("minleafsize   : " + minleafsize);
        optionLogger.info("schemafile    : " + schemaFile);
        optionLogger.info("subsample     : "
                + ((subsamplesize == 0) ? "All examples" : Integer.toString(subsamplesize)));
        optionLogger.info("subsample inc : " + subsampleincreasement);
        optionLogger.info("increase after: " + subsampleincreaseafter);

        optionLogger.info("CRF parameters");
        optionLogger.info("crftrainsteps : " + crftrainsteps);
        optionLogger.info("windowSize    : " + windowSize);
        optionLogger.info("bg knowledge  : " + backgroundknowledgeFile);
        
        optionLogger.info("improvements    : " + improvements);

        // read the data
        InterpretationExampleContainer trainExamplesTagging = null;
        InterpretationExampleContainer testExamplesTagging = null;
        ClassificationExampleContainer trainExamplesClassification = null;
        ClassificationExampleContainer testExamplesClassification = null;
        ClassificationExampleContainer validationExamplesClassification = null;

        if (line.hasOption("data")) {
            // n-fold cross validation

            if (line.hasOption("test") || line.hasOption("train")) {
                showHelp("if you use data you cannot used test or train");
                System.exit(1);
            }

            if (folds < 2) {
                showHelp("Illegal value for folds, value must be an integer greater 2");
                System.exit(1);
            }

            if (fold < 0 || fold >= folds) {
                showHelp("Illegal value for fold, value must be an integer in the range 0<=X<folds");
                System.exit(1);
            }

            optionLogger.info(Integer.toString(folds) + "-fold cross validation, testfold is "
                    + Integer.toString(fold));

            String[] entries = line.getOptionValues("data");
            if (entries == null || entries.length == 0) {
                showHelp("no entry at data parameter");
                System.exit(1);
            }

            // read the data from the files
            // and split into test and training data
            if (mode.equals(MasterInterpretation.MODETAGGING)) {
                InterpretationExampleContainer tmp = MasterInterpretation.processTaggingExamples(preparationLogger, entries);
                trainExamplesTagging = tmp.getSubfoldInverse(folds, fold, seed);
                testExamplesTagging = tmp.getSubfold(folds, fold, seed);
            } else {
                ClassificationExampleContainer tmp = MasterInterpretation.processClassificationExamples(preparationLogger,
                        entries);
                trainExamplesClassification = tmp.getSubfoldInverse(folds, fold, seed);
                testExamplesClassification = tmp.getSubfold(folds, fold, seed);
                
                trainExamplesClassification.sortClassAtoms();
                testExamplesClassification.sortClassAtoms();
            }

        } else if (line.hasOption("test") && line.hasOption("train")) {
            // test and training data specified separately
            optionLogger.info("test and training data specified separately");

            // read the data from the files
            if (mode.equals(MasterInterpretation.MODETAGGING)) {
                trainExamplesTagging = MasterInterpretation.processTaggingExamples(preparationLogger, line
                        .getOptionValues("train"));
                testExamplesTagging = MasterInterpretation.processTaggingExamples(preparationLogger, line
                        .getOptionValues("test"));
            } else {
                trainExamplesClassification = MasterInterpretation.processClassificationExamples(preparationLogger, line
                        .getOptionValues("train"));
                testExamplesClassification = MasterInterpretation.processClassificationExamples(preparationLogger, line
                        .getOptionValues("test"));
                trainExamplesClassification.sortClassAtoms();
                testExamplesClassification.sortClassAtoms();
            }
        } else {
            showHelp("You must specify either test and training data or say to use n-fold cross validation");
            System.exit(1);
        }
        
        if (line.hasOption("validation")) {
            optionLogger.info("validation sets specified");
            if (mode.equals(MasterInterpretation.MODETAGGING)) {
                throw new IllegalStateException("A validation set for tagging mode is not allowed");
            } else {
                validationExamplesClassification = MasterInterpretation.processClassificationExamples(preparationLogger, line
                        .getOptionValues("validation"));
            }
            
        }

        // this atoms are needed for the One Against All and Round Robin Mode
        Atom targetAtom = new Atom(new Constant("classTarget"));
        Atom othersAtom = new Atom(new Constant("classOthers"));

        // read term schemata if provided as parameter
        List<TermSchema> schemata = null;
        if (schemaFile != null) {
            preparationLogger.info("read schema-file: " + schemaFile);
            schemata = XMLInput.readSchemata(schemaFile);
            preparationLogger.info("Schemafile contained " + schemata.size() + " schemata");

            // add the class-atoms in classification-mode
            // FIXME user has to specify class-atoms in tagging mode by himself
            // in schema file!
            if (mode.equals(MasterInterpretation.MODECLASSIFICATION)) {
                // we add only class atoms from training files, because other
                // atoms can't occur in the regression examples
                for (Atom a : trainExamplesClassification.getClassAtoms())
                    schemata.add(new TermSchema(a.getTermRepresentation(), WindowMaker.FIELDOUTPUT));
            }

            // in OAA or RR mode the original class atoms are not used
            // instead the regression examples contain targetAtom or othersAtom
            // we must add these atom as schema, that they can be used as tests
            // in the regression tree. But because of the binary character of
            // them, we must add only one.
            if (mode.equals(MasterInterpretation.MODECLASSIFICATIONOAA) || mode.equals(MasterInterpretation.MODECCLASSIFICATIONRR)) {
                schemata.add(new TermSchema(targetAtom.getTermRepresentation(), WindowMaker.FIELDOUTPUT));
            }
        }

        WindowMaker wm;
        if (backgroundknowledgeFile == null) {
            wm = new WindowMaker(windowSize);
        } else {
            wm = XMLInput.makeWindowMakerWithBGKnowledge(backgroundknowledgeFile, windowSize);
            // we need the "true-atom" as schema, because true/false atoms are
            // added at every window
            if (schemata != null)
                schemata.add(new TermSchema(wm.getTrueAtom().getTermRepresentation(),
                        WindowMaker.FIELDDIVERSE));
        }

        if (schemata != null) {
            // add the atoms for start and stop
            //schemata.add(new TermSchema(wm.getStartAtom().getTermRepresentation(), WindowMaker.FIELDINPUT));
            //schemata.add(new TermSchema(wm.getStopAtom().getTermRepresentation(), WindowMaker.FIELDINPUT));
        }

        preparationLogger.info("windowMaker    : " + wm);
        preparationLogger.info("schemata : " + schemata);
        
        /*begin dirty*/
        String bgn = "test(same)." + "test(outIs(classTarget))." + "test(outIs(classOthers))."
                + "test(outoldis(Y)) :- test(outis(Y))." 
                + "test(inputis(Pos,Elem)) :-"
                + "   outputPositions(Positions),"
                + "   member(Pos,Positions),"
                + "   possibleInputs(Elem)."
                + "possibleInputs(strand(Name,Type,Length)) :-"
                + "   member(Type,[plus,minus,null,SomeType]),"
                + "   member(Length,[small,medium,short,SomeLength])."
                + "possibleInputs(helix(SomeHelix,Length)) :-"
                + "   member(Length,[small,medium,short,SomeLength])."
                + "possibleInputs(helix(h(Orientation,Type),Length)) :-"
                + "   member(Length,[small,medium,large]),"
                + "   member(Orientation,[left,right,SomeOrientation]),"
                + "   member(Type,[alpha,f3to10,SomeType])."
                + "possibleInputs(sequence_start)."
                + "possibleInputs(sequence_end)."
                + "succeds(test(same),[X,X|_])."
                + "succeds(test(outis(X)),[_,X|_])."
                + "succeds(test(outoldis(X)),[X,_|_])."
                + "succeds(test(inputis(Pos,Elem)),Window):-" 
                + "   nth0(Pos,Window,Elem)."
                + "succeds(not(Test),Window):-"
                + "   not(succeds(Test,Window)).";
        /*end dirty*/

        //RegressionModelTrainer<List<Atom>> trainer = new TrainerWrapper<List<Atom>>(
        //      new PrologRegressionTreeTrainer(treedepth, minleafsize, bgn, wm.getOutputFields()), seed,
        //      subsamplesize, subsampleincreaseafter, subsampleincreasement);
        
        
        RegressionModelTrainer<Interpretation> trainer = new TrainerWrapper<Interpretation>(
                
                new InterpretationRegressionTreeTrainerBestFirst(treedepth, minleafsize, schemata),  seed,
                
                subsamplesize, subsampleincreaseafter, subsampleincreasement);
        LogicalCountingTreeTrainer trainer2 = new LogicalCountingTreeTrainer(treedepth, minleafsize, schemata);

        // we have all parameters and can now start the chosen operation
        // mode
        if (mode.equals(MasterInterpretation.MODETAGGING)) {
            new ModeTaggingInterpretation(trainExamplesTagging, testExamplesTagging, seed, trainer, wm, trainer2,
                    crftrainsteps);
        } else if (mode.equals(MasterInterpretation.MODECLASSIFICATION)) {
    /*        new ModeClassification(trainExamplesClassification, testExamplesClassification, validationExamplesClassification, improvements,seed, trainer,
                    wm, trainer2, crftrainsteps);*/
        } else if (mode.equals(MasterInterpretation.MODECLASSIFICATIONOAA)) {
            /*new ModeClassificationOAA(trainExamplesClassification, testExamplesClassification, validationExamplesClassification, improvements,seed, trainer,
                    wm, trainer2, crftrainsteps, targetAtom, othersAtom);*/
        } else if (mode.equals(MasterInterpretation.MODECCLASSIFICATIONRR)) {
            /*new ModeClassificationRR(trainExamplesClassification, testExamplesClassification, validationExamplesClassification, improvements,seed, trainer,
                    wm, trainer2, crftrainsteps, targetAtom, othersAtom);*/
        } else {
            // should actually never happen because we have almost trapped this
            // case, but who knows ...
            showHelp("Unknown mode " + mode);
            System.exit(1);
        }

    }

    /**
     * Shows the paramter for the command line. If errText is given it is
     * printed out to stdErr.
     * 
     * @param errText
     *            optional error message. May be null.
     */
    private static void showHelp(String errText) {
        HelpFormatter f = new HelpFormatter();

        f.printHelp("lcrf", "header", getOptions(), "footer", true);

        if (errText != null && !errText.equals("")) {
            System.err.println(errText);
        }
    }

}
